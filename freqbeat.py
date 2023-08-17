import requests
import numpy as np
import av
import time
import os
import yaml
import keyboard
import pygetwindow as gw

ASCII_ART = """
   ___________                   __________               __   
   \_   _____/_____   ____  _____\______   \ ____ _____ _/  |_  
    |    __|\_  __ \_/ __ \/ ____/|    |  _/| __ |\__  \|    _\  
    |    \   |  | \/\  ___/| |_| ||    |   \  ___/ / __ \|  |  
    \__  /   |__|    \___ \ \__  ||______  /\___ \/____  /__|  
       \/                \/    \_\       \/     \/     \/      
"""

# Function to Load Configuration
def load_config():
    try:
        with open('config.yaml', 'r') as file:
            return yaml.safe_load(file)
    except Exception as e:
        print(f"Error loading configuration: {e}")
        exit()
        
# Function to Save Speed to Configuration
def save_speed_to_config(speed):
    with open('config.yaml', 'w') as file:
        yaml.dump({'Speed': speed}, file)

# Function to Extract Stream URL
def get_stream_url(url):
    try:
        if url.endswith('.m3u') or url.endswith('.pls'):
            response = requests.get(url, timeout=10)
            lines = response.text.splitlines()
            for line in lines:
                if not line.startswith("#") and "http" in line:
                    return line
        else:
            return url
    except requests.RequestException as e:
        print(f"Error fetching the URL: {e}")
        return None

# Function to Analyze and Display Stream Data
def analyze_stream(url, speed):
    speeds = [1, 2, 3, 4]
    stream_url = get_stream_url(url)
    if not stream_url:
        print("Unable to extract stream URL.")
        return
    reconnect_attempts = 0
    while reconnect_attempts < 10:
        try:
            container = av.open(stream_url)
            audio_stream = next(s for s in container.streams if s.type == 'audio')
            sample_rate = audio_stream.sample_rate
            while True:
                start_time = time.time()
                process_stream_data(container, audio_stream, sample_rate, speed, speeds, stream_url)
                elapsed_time = time.time() - start_time
                sleep_duration = max(1.0/speed - elapsed_time, 0)
                time.sleep(sleep_duration)
            reconnect_attempts = 0
        except (av.error.HTTPError, av.error.FFmpegError) as e:
            if "[Errno 5] I/O error" in str(e):
                print("Encountered an I/O error. Attempting to reconnect...")
                reconnect_attempts += 1
                print(f"Attempting to reconnect ({reconnect_attempts}/10)...")
                time.sleep(1)
            else:
                print(f"Error: {e}")
                reconnect_attempts += 1
                print(f"Attempting to reconnect ({reconnect_attempts}/10)...")
                time.sleep(1)
            if reconnect_attempts == 10:
                print("Failed to reconnect after 10 attempts. Returning to URL prompt.")
                time.sleep(3)
                prompt_for_url()
                return

# Function to Process and Display Stream Data
def process_stream_data(container, audio_stream, sample_rate, speed, speeds, stream_url):
    try:
        frame = next(container.decode(audio_stream))
        audio_data = frame.to_ndarray().flatten()
        mono_channel = (audio_data[0::2] + audio_data[1::2]) / 2
        chunk_size = int(sample_rate / speed)
        freq, dominant_low, dominant_med, dominant_high = analyze_frequencies(mono_channel, sample_rate)
        quiet, normal, loud = analyze_volume(mono_channel)
        display_output(sample_rate, chunk_size, speed, dominant_low, dominant_med, dominant_high, quiet, normal, loud)
        handle_user_input(speeds, speed)
    except StopIteration:
        print("Stream ended.")
    except av.error.FFmpegError as e:
        if "[Errno 5] I/O error" in str(e):
            raise e
        else:
            print(f"Error during stream decoding: {e}")
    except Exception as e:
        print(f"Error during stream decoding: {e}")

# Function to Analyze Frequencies
def analyze_frequencies(mono_channel, sample_rate):
    freq = np.fft.rfftfreq(mono_channel.size, d=1/sample_rate)
    fft_vals = np.abs(np.fft.rfft(mono_channel))

    third_len = len(freq) // 3
    dominant_low = int(freq[np.argmax(fft_vals[:third_len])])
    dominant_med = int(freq[third_len + np.argmax(fft_vals[third_len:2*third_len])])
    dominant_high = int(freq[2*third_len + np.argmax(fft_vals[2*third_len:])])

    return freq, dominant_low, dominant_med, dominant_high

# Function to Analyze Volume Levels
def analyze_volume(mono_channel):
    avg_volume = np.mean(np.abs(mono_channel))
    loud = "*" if avg_volume > 0.95 else " "
    quiet = "*" if avg_volume < 0.05 else " "
    normal = "*" if 0.05 <= avg_volume <= 0.95 else " "
    return quiet, normal, loud

# Function to Display the Output
def display_output(sample_rate, chunk_size, speed, dominant_low, dominant_med, dominant_high, quiet, normal, loud):
    os.system('cls' if os.name == 'nt' else 'clear')
    print(ASCII_ART)
    print(f"\n                       Speed: 1/{speed}, Chunk: {chunk_size // 1024}KB")
    print(f"\n               Channels: 2, Bits: 16Bit, Rate: {sample_rate//1000}Khz")
    print(f"                  Quiet [{quiet}], Normal [{normal}], Loud [{loud}]")
    print(f"               Low: {dominant_low}Hz, Med: {dominant_med}Hz, High: {dominant_high}Hz")

    print("\n\n                       Press any key for Menu")

# Function to Handle User Input
def handle_user_input(speeds, speed):
    current_window = gw.getActiveWindow()
    if "python" not in current_window.title.lower():
        return
    if keyboard.is_pressed('s'):
        new_speed = change_speed_prompt(speeds, speed)
        return new_speed
    elif keyboard.is_pressed('q'):
        exit()
    return speed

# Function to Prompt User for URL Input
def prompt_for_url():
    config = load_config()
    speed = config.get('Speed', 1)
    os.system('cls' if os.name == 'nt' else 'clear')
    print(ASCII_ART)
    print(f"\n                     Speed: {speed} updates/second")
    url_or_speed = input("\n\n          Enter Url, Speed = 1/2/3/4, Quit Program = Q: ")
    if url_or_speed.lower() == 'q':
        exit()
    elif url_or_speed in ['1', '2', '3', '4']:
        new_speed = int(url_or_speed)
        save_speed_to_config(new_speed)
        prompt_for_url()
    else:
        analyze_stream(url_or_speed, speed)

if __name__ == "__main__":
    prompt_for_url()
