import requests
import numpy as np
import av
import time
import os
import yaml
import keyboard
import pygetwindow as gw

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
    speeds = [1, 2, 4, 8]
    stream_url = get_stream_url(url)
    if not stream_url:
        print("Unable to extract stream URL.")
        return
    try:
        container = av.open(stream_url)
        audio_stream = next(s for s in container.streams if s.type == 'audio')
        sample_rate = audio_stream.sample_rate
    except (av.error.HTTPError, av.error.FFmpegError, StopIteration) as e:
        print(f"Error: {e}")
        return

    while True:
        start_time = time.time()
        process_stream_data(container, audio_stream, sample_rate, speed, speeds)
        elapsed_time = time.time() - start_time
        sleep_duration = max(1/speed - elapsed_time, 0)
        time.sleep(sleep_duration)

# Function to Process and Display Stream Data
def process_stream_data(container, audio_stream, sample_rate, speed, speeds):
    try:
        frame = next(container.decode(audio_stream))
        audio_data = frame.to_ndarray().flatten()
        mono_channel = (audio_data[0::2] + audio_data[1::2]) / 2
        chunk_size = int(sample_rate / speed)
        freq, dominant_low, dominant_med, dominant_high = analyze_frequencies(mono_channel, sample_rate)
        quiet, normal, loud = analyze_volume(mono_channel)  # Updated this line
        display_output(sample_rate, chunk_size, speed, dominant_low, dominant_med, dominant_high, quiet, normal, loud)
        handle_user_input(speeds, speed)
    except StopIteration:
        print("Stream ended.")
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
    fft_vals = np.abs(np.fft.rfft(mono_channel))
    max_val = max(fft_vals)
    loud = "*" if max_val > 0.90 * max_val else " "
    quiet = "*" if max_val < 0.1 * max_val else " "
    normal = "*" if 0.1 * max_val <= max_val <= 0.90 * max_val else " "
    return quiet, normal, loud

# Function to Display the Output
def display_output(sample_rate, chunk_size, speed, dominant_low, dominant_med, dominant_high, quiet, normal, loud):
    os.system('cls' if os.name == 'nt' else 'clear')
    print("\n\n                     FreqBeat")
    print(f"\n\n       Channels: 2, Bits: 16Bit, Rate: {sample_rate//1000}Khz")  # Updated this line
    print(f"          Quiet [{quiet}], Normal [{normal}], Loud [{loud}]")
    print(f"      Low: {dominant_low}Hz, Med: {dominant_med}Hz, High: {dominant_high}Hz")
    print(f"\n            Speed: 1/{speed}s, Chunk: {chunk_size // 1024}KB")
    print("\n\n  Slower = <, Faster = >, New Url = n, Quit = q")

# Function to Handle User Input
def handle_user_input(speeds, speed):
    current_window = gw.getActiveWindow()
    if "python" not in current_window.title.lower():
        return
    if keyboard.is_pressed(','):
        speed_idx = speeds.index(speed)
        if speed_idx > 0:
            speed = speeds[speed_idx - 1]
            save_speed_to_config(speed)
    elif keyboard.is_pressed('.'):
        speed_idx = speeds.index(speed)
        if speed_idx < len(speeds) - 1:
            speed = speeds[speed_idx + 1]
            save_speed_to_config(speed)
    elif keyboard.is_pressed('n'):
        prompt_for_url()
    elif keyboard.is_pressed('q'):
        exit()

# Function to Prompt User for URL Input
def prompt_for_url():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("\n\n                    FreqBeat")
    url = input("\nEnter Url or Q for Quit: ")
    if url.lower() == 'q':
        exit()
    elif url:
        config = load_config()
        speed = config.get('Speed', 1)
        analyze_stream(url, speed)

if __name__ == "__main__":
    prompt_for_url()
