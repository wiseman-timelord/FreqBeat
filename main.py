# main.py

# Imports
import threading
import queue
import requests
from requests.exceptions import HTTPError, Timeout, RequestException
import numpy as np
import av
import time
import yaml
import keyboard
import pygetwindow as gw
import loop
import platform
import os

# Set window title to StatStream
if platform.system() == "Windows":
    os.system("title StatStream")
elif platform.system() == "Linux":
    print("\033]0;StatStream\007", end='', flush=True)

# Ascii Art for the console display
ASCII_ART = r"""
     _________ __          __   _________ __                                 
    /   _____//  |______ _/  |_/   _____//  |________   ____ _____    _____  
    \_____  \\   __\__  \\   __\_____  \\   __\_  __ \_/ __ \\__  \  /     \ 
    /        \|  |  / __ \|  | /        \|  |  |  | \/\  ___/ / __ \|  Y Y  \
   /_______  /|__| |____  /__|/_______  /|__|  |__|    \___ \|____  /__|_|  /
           \/           \/            \/                   \/     \/      \/ 
"""

# Load configuration from 'config.yaml'
def load_config():
    try:
        with open('config.yaml', 'r') as file:
            return yaml.safe_load(file)
    except Exception as e:
        print(f"Error loading configuration: {e}")
        exit()

# Save the speed setting to 'config.yaml'
def save_speed_to_config(speed):
    try:
        with open('config.yaml', 'w') as file:
            yaml.dump({'Speed': speed}, file)
    except Exception as e:
        print(f"Error saving configuration: {e}")
        exit()

# Main menu for user input
def prompt_for_url():
    config = load_config()
    speed = config.get('Speed', 1)
    # os.system('cls' if os.name == 'nt' else 'clear')
    print(ASCII_ART)
    print(f"\n\n\n                             Speed: {speed} updates/second")
    url_or_speed = input("\n\n\n\n Enter Url, Speed = 1/2/3/4, Quit = Q: ")
    if url_or_speed.lower() == 'q':
        exit()
    elif url_or_speed in ['1', '2', '3', '4']:
        new_speed = int(url_or_speed)
        save_speed_to_config(new_speed)
        prompt_for_url()
    else:
        return url_or_speed

# Extract the stream URL from the given URL
def get_stream_url(url):
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        # Make a GET request with stream=True to check if the URL is valid
        response = requests.get(url, headers=headers, timeout=10, stream=True)
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx and 5xx)

        # Close the response stream to free up resources
        response.close()

        # Check if the URL ends with .m3u or .pls and extract the stream URL
        if url.endswith('.m3u') or url.endswith('.pls'):
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            lines = response.text.splitlines()
            for line in lines:
                if not line.startswith("#") and "http" in line:
                    return line
        else:
            return url

    except HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except Timeout as timeout_err:
        print(f"Timeout error: {timeout_err}")
    except RequestException as req_err:
        print(f"An error occurred while fetching the URL: {req_err}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

    return None


# Analyze and display the stream data
def analyze_stream(container, audio_stream, sample_rate, speed, speeds, stream_url, key_queue):
    try:
        frame = next(container.decode(audio_stream))
        audio_data = frame.to_ndarray().flatten()
        mono_channel = (audio_data[0::2] + audio_data[1::2]) / 2
        chunk_size = int(sample_rate / speed)
        freq, dominant_low, dominant_med, dominant_high = analyze_frequencies(mono_channel, sample_rate)
        quiet, normal, loud = analyze_volume(mono_channel)
        display_output(sample_rate, chunk_size, speed, dominant_low, dominant_med, dominant_high, quiet, normal, loud)
        new_speed = handle_user_input(key_queue, speeds, speed)
        return new_speed
    except StopIteration:
        print("Stream ended.")
    except av.error.FFmpegError as e:
        if "[Errno 5] I/O error" in str(e):
            raise e
        else:
            print(f"Error during stream decoding: {e}")
    except Exception as e:
        print(f"Error during stream decoding: {e}")

# Analyze the frequencies in the audio stream
def analyze_frequencies(mono_channel, sample_rate):
    freq = np.fft.rfftfreq(mono_channel.size, d=1/sample_rate)
    fft_vals = np.abs(np.fft.rfft(mono_channel))
    third_len = len(freq) // 3
    dominant_low = int(freq[np.argmax(fft_vals[:third_len])])
    dominant_med = int(freq[third_len + np.argmax(fft_vals[third_len:2*third_len])])
    dominant_high = int(freq[2*third_len + np.argmax(fft_vals[2*third_len:])])
    return freq, dominant_low, dominant_med, dominant_high
    
# Analyze the volume levels in the audio stream
def analyze_volume(mono_channel):
    avg_volume = np.mean(np.abs(mono_channel))
    loud = "*" if avg_volume > 0.95 else " "
    quiet = "*" if avg_volume < 0.05 else " "
    normal = "*" if 0.05 <= avg_volume <= 0.95 else " "
    return quiet, normal, loud    

# Display the output on the console
def display_output(sample_rate, chunk_size, speed, dominant_low, dominant_med, dominant_high, quiet, normal, loud):
    os.system('cls' if os.name == 'nt' else 'clear')
    print(ASCII_ART)
    print(f"\n                           Speed: 1/{speed}, Chunk: {chunk_size // 1024}KB")
    print(f"\n                   Channels: 2, Bits: 16Bit, Rate: {sample_rate//1000}Khz")
    print(f"                      Quiet [{quiet}], Normal [{normal}], Loud [{loud}]")
    print(f"                   Low: {dominant_low}Hz, Med: {dominant_med}Hz, High: {dominant_high}Hz")
    print("\n\n                           Press any key for Menu")

# Handle user input for changing speed or quitting
def handle_user_input(key_queue, speeds, speed):
    if not key_queue.empty():
        key = key_queue.get()
        if key == 's':
            new_speed = change_speed_prompt(speeds, speed)
            return new_speed
        elif key == 'q':
            exit()
    return speed


# Prompt user to change the speed
def change_speed_prompt(speeds, current_speed):
    print("Current speed options are:", speeds)
    new_speed = input("Enter new speed: ")
    if new_speed in map(str, speeds):
        return int(new_speed)
    else:
        print("Invalid speed. Keeping the current speed.")
        return current_speed

if __name__ == "__main__":
    key_queue = queue.Queue()
    
    while True:  # Wrap in a loop to return to the main menu
        # Clear the key_queue when returning to the main menu
        key_queue.queue.clear()
        
        url = prompt_for_url()
        config = load_config()
        speed = config.get('Speed', 1)
        speeds = [1, 2, 3, 4]
        
        try:
            loop.main_loop(url, speed, get_stream_url, analyze_stream, key_queue, speeds)
        except Exception as e:
            print(f"An error occurred: {e}")
            print("Returning to the main menu...")
