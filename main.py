# Script "main.py"...

# Imports
import threading
import queue
import requests
import numpy as np
import av
import time
import yaml
import keyboard
import pygetwindow as gw
import platform
import os
import librosa
from requests.exceptions import HTTPError, Timeout, RequestException
from urllib.parse import urlparse, parse_qs

# Set window title to StatStream
if platform.system() == "Windows":
    os.system("title StatStream")
elif platform.system() == "Linux":
    print("\033]0;StatStream\007", end='', flush=True)

# Globals
keyboard_thread = None
current_bpm = 0
min_bpm = 0
max_bpm = 0
bpm_lock = threading.Lock()

# Ascii Art for the console display
ASCII_ART = r"""
     _________ __          __   _________ __                                 
    /   _____//  |______ _/  |_/   _____//  |________   ____ _____    _____  
    \_____  \\   __\__  \\   __\_____  \\   __\_  __ \_/ __ \\__  \  /     \ 
    /        \|  |  / __ \|  | /        \|  |  |  | \/\  ___/ / __ \|  Y Y  \
   /_______  /|__| |____  /__|/_______  /|__|  |__|    \___ \|____  /__|_|  /
           \/           \/            \/                   \/     \/      \/ 
"""

# Custom exception to signal a return to the main menu
class ReturnToMenuException(Exception):
    pass

# Listen for keyboard input and add it to the queue
def keyboard_input_listener(key_queue, stop_event):
    while not stop_event.is_set():
        current_window = gw.getActiveWindow()
        if "StatStream" in current_window.title:
            key = keyboard.read_key(suppress=True)
            key_queue.put(key)
        time.sleep(0.1)

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

# Sanitize and format the URL
def sanitize_url(url):
    print("Debug: Sanitizing URL...")
    url = url.strip()  # Remove leading and trailing whitespaces
    if not url.startswith(('http://', 'https://', 'rtsp://', 'mms://')):
        print("Debug: Adding 'http://' to the URL.")
        url = 'http://' + url  # Add http if missing
    print(f"Debug: Sanitized URL - {url}")
    return url

# Main menu for user input
def prompt_for_url():
    config = load_config()
    speed = config.get('Speed', 1)
    os.system('cls' if os.name == 'nt' else 'clear')
    print(ASCII_ART)
    print(f"\n                             Speed: {speed} updates/second")
    url_or_speed = input("\n\n Enter Url, Speed = 1/2/3/4, Quit = Q: ")
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
    print("Debug: Entering get_stream_url function.")  # Added Debug statement
    url = sanitize_url(url)  # Sanitize the URL
    headers = {'User-Agent': 'Mozilla/5.0'}
    parsed_url = urlparse(url)
    print(f"Debug: Parsed URL - {parsed_url}")  # Existing Debug statement
    
    try:
        print("Debug: About to make a GET request...")  # Existing Debug statement
        response = requests.get(url, headers=headers, timeout=10, stream=True)
        response.raise_for_status()
        response.close()
        print("Debug: GET request successful.")  # Existing Debug statement

        if url.endswith(('.m3u', '.pls', '.mp3', '.aac', '.ogg', '.flac')):
            print("Debug: Handling playlist or direct audio URLs.")  # Existing Debug statement
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            lines = response.text.splitlines()
            if not lines:
                print("Debug: No lines found in the playlist.")
                return None
            for line in lines:
                if not line.startswith("#") and "http" in line:
                    print(f"Returning extracted URL: {line}")
                    return line
        elif parsed_url.scheme in ['rtsp', 'mms']:
            print(f"Debug: Handling protocol-specific URL: {url}")
            return url
        elif parsed_url.query:
            print(f"Debug: Handling parameterized URL: {url}")
            return url
        elif parsed_url.port:
            print(f"Debug: Handling port-specified URL: {url}")
            return url
        elif parsed_url.path:
            print(f"Debug: Handling path-based URL: {url}")
            return url
        elif parsed_url.hostname and '.' not in parsed_url.hostname:
            print(f"Debug: Handling IP address URL: {url}")
            return url
        else:
            print(f"Debug: Handling original URL: {url}")
            return url
    except HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except Timeout as timeout_err:
        print(f"Timeout error: {timeout_err}")
    except RequestException as req_err:
        print(f"An error occurred while fetching the URL: {req_err}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    print("Debug: Exiting get_stream_url function.")
    return None

# Function to analyze frequencies
def analyze_frequencies(audio_data, sample_rate):
    D = librosa.stft(audio_data)
    freqs = librosa.fft_frequencies(sr=sample_rate)
    magnitude = np.abs(D)
    low_freqs = magnitude[(freqs >= 20) & (freqs <= 300)]
    med_freqs = magnitude[(freqs > 300) & (freqs <= 3000)]
    high_freqs = magnitude[(freqs > 3000) & (freqs <= 20000)]
    dominant_low = freqs[np.argmax(low_freqs)]
    dominant_med = freqs[np.argmax(med_freqs)]
    dominant_high = freqs[np.argmax(high_freqs)]
    return dominant_low, dominant_med, dominant_high

# Function to analyze volume
def analyze_volume(audio_data):
    rms_value = np.sqrt(np.mean(np.square(audio_data)))
    if rms_value < 0.1:
        return "Quiet", 0, 0
    elif rms_value < 0.9:
        return 0, "Normal", 0
    else:
        return 0, 0, "Loud"

# Analyze and display the stream data
def analyze_stream(container, audio_stream, sample_rate, speed, speeds, stream_url, key_queue):
    global current_bpm, min_bpm, max_bpm
    try:
        frame = next(container.decode(audio_stream))
        audio_data = frame.to_ndarray().flatten()
        quiet_stereo, normal_stereo, loud_stereo = analyze_volume(audio_data)
        print("Debug: Completed volume analysis for stereo channel.")
        mono_channel = (audio_data[0::2] + audio_data[1::2]) / 2
        chunk_size = int(sample_rate / speed)
        quiet_mono, normal_mono, loud_mono = analyze_volume(mono_channel)
        print("Debug: Completed volume analysis for mono channel.")
        onset_env = librosa.onset.onset_strength(y=mono_channel, sr=sample_rate)
        print("Debug: Onset strength calculated.")
        tempo, _ = librosa.beat.beat_track(onset_envelope=onset_env, sr=sample_rate)
        print("Debug: Tempo calculated.")
        with bpm_lock:
            current_bpm = tempo
            if tempo < min_bpm or min_bpm == 0:
                min_bpm = tempo
            if tempo > max_bpm:
                max_bpm = tempo
        print("Debug: Updated BPM range.")
        dominant_low, dominant_med, dominant_high = analyze_frequencies(mono_channel, sample_rate)
        print("Debug: Frequencies analyzed.")
        display_output(sample_rate, chunk_size, speed, dominant_low, dominant_med, dominant_high, quiet_mono, normal_mono, loud_mono)
        print("Debug: Completed output display.")
        new_speed = handle_user_input(key_queue, speeds, speed)
        print("Debug: Completed user input handling.")
        print("Debug: Exiting analyze_stream function.")
        return new_speed
    except StopIteration:
        print("Stream ended.")
    except av.error.FFmpegError as e:
        if "[Errno 5] I/O error" in str(e):
            raise e
        else:
            print(f"Error during stream decoding: {e}")
    except Exception as e:
        print(f"An exception occurred in analyze_stream: {e}")

# Display the output on the console
def display_output(sample_rate, chunk_size, speed, dominant_low, dominant_med, dominant_high, quiet, normal, loud):
    os.system('cls' if os.name == 'nt' else 'clear')
    print(ASCII_ART)
    print(f"\nSpeed: 1/{speed}, Chunk: {chunk_size // 1024}KB")
    print(f"Channels: 2, Bits: 16Bit, Rate: {sample_rate//1000}Khz")
    print(f"Quiet [{quiet}], Normal [{normal}], Loud [{loud}]")
    print(f"Low: {dominant_low}Hz, Med: {dominant_med}Hz, High: {dominant_high}Hz")
    print(f"BPM: {current_bpm}, BPM Range: {min_bpm}-{max_bpm}")
    print("\nPress any key for Menu")

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

# Main loop for handling the audio stream
def main_loop(url, speed, get_stream_url, analyze_stream, key_queue, speeds):
    print("Debug: Entering main_loop function.")
    global keyboard_thread
    stop_event = None
    
    try:
        print("Debug: About to sanitize the URL...")
        url = sanitize_url(url)  # Sanitize the URL
        print("Debug: About to fetch the stream URL...")
        stream_url = get_stream_url(url)
        if not stream_url:
            print("Debug: Stream URL is None. Returning to main menu.")
            return
        print(f"Debug: Fetched stream URL - {stream_url}")
        reconnect_attempts = 0
        if keyboard_thread is not None and stop_event is not None:
            stop_event.set()
            keyboard_thread.join()
        stop_event = threading.Event()
        keyboard_thread = threading.Thread(target=keyboard_input_listener, args=(key_queue, stop_event))
        keyboard_thread.daemon = True
        keyboard_thread.start()
        while reconnect_attempts < 10:
            try:
                print("Debug: About to open stream...")
                container = av.open(stream_url)
                print("Debug: Stream opened.")
                audio_stream = next(s for s in container.streams if s.type == 'audio')
                sample_rate = audio_stream.sample_rate
                while True:
                    if not key_queue.empty():
                        key = key_queue.get()
                        if key == 'q':
                            return
                        else:
                            raise ReturnToMenuException
                    start_time = time.time()
                    print("Debug: About to call analyze_stream.")
                    analyze_stream(container, audio_stream, sample_rate, speed, speeds, stream_url, key_queue)
                    elapsed_time = time.time() - start_time
                    sleep_duration = max(1.0/speed - elapsed_time, 0)
                    time.sleep(sleep_duration)
            except (av.error.HTTPError, av.error.FFmpegError) as e:
                print(f"Error: {e}")
                reconnect_attempts += 1
                print(f"Attempting to reconnect ({reconnect_attempts}/10)...")
                time.sleep(1)
                if reconnect_attempts == 10:
                    print("Failed to reconnect after 10 attempts. Returning to URL prompt.")
                    time.sleep(3)
                    return
    except ReturnToMenuException:
        print("Returning to the main menu...")
        if keyboard_thread is not None:
            stop_event.set()
            keyboard_thread.join()
        return
    except Exception as e:
        print(f"Debug: An exception occurred in main_loop: {e}")


if __name__ == "__main__":
    key_queue = queue.Queue()
    current_bpm = 0
    min_bpm = 0
    max_bpm = 0
    keyboard_thread = None
    while True:
        key_queue.queue.clear()
        url = prompt_for_url()
        config = load_config()
        speed = config.get('Speed', 1)
        speeds = [1, 2, 3, 4]
        try:
            main_loop(url, speed, get_stream_url, analyze_stream, key_queue, speeds)
        except Exception as e:
            print(f"An error occurred: {e}")
            print("Returning to the main menu...")
