import requests
import numpy as np
import av
import time
import os

# Function to Extract URL
def get_stream_url(url):
    if url.endswith('.m3u') or url.endswith('.pls'):
        response = requests.get(url, timeout=10)
        lines = response.text.splitlines()
        for line in lines:
            if not line.startswith("#") and "http" in line:
                return line
    else:
        return url
    return None

# Function to Analyze Stream
def analyze_stream(url):
    stream_url = get_stream_url(url)
    if not stream_url:
        print("Unable to extract stream URL.")
        return
    try:
        container = av.open(stream_url)
    except av.error.HTTPError as e:
        print(f"Failed to open the stream due to HTTP error: {e}")
        return
    except av.error.FFmpegError as e:
        print(f"Failed to open the stream due to FFmpeg error: {e}")
        return
    except Exception as e:
        print(f"Failed to open the stream due to an unexpected error: {e}")
        return

    try:
        audio_stream = next(s for s in container.streams if s.type == 'audio')
    except StopIteration:
        print("No audio stream found in the provided URL.")
        return

    try:
        for frame in container.decode(audio_stream):
            audio_data = frame.to_ndarray().flatten()
            left_channel = audio_data[0::2]
            right_channel = audio_data[1::2]
            left_freq = np.fft.rfftfreq(left_channel.size, d=1/44100)
            right_freq = np.fft.rfftfreq(right_channel.size, d=1/44100)
            left_fft_vals = np.abs(np.fft.rfft(left_channel))
            right_fft_vals = np.abs(np.fft.rfft(right_channel))
            left_dominant_freq = left_freq[np.argmax(left_fft_vals)]
            right_dominant_freq = right_freq[np.argmax(right_fft_vals)]
            os.system('cls' if os.name == 'nt' else 'clear')
            print("\n\n")
            print("                    FreqBeat")
            print("\n\n      Chan: 2, Bits: 16Bit, Rate: 44Khz")
            print("\n            Left  Freq.: {:.2f}Hz".format(left_dominant_freq))
            print("            Right Freq.: {:.2f}Hz".format(right_dominant_freq))
            time.sleep(1)
    except av.error.InvalidDataError:
        print("Invalid or corrupted data encountered in the audio stream.")
    except Exception as e:
        print(f"An error occurred while processing the audio stream: {e}")

if __name__ == "__main__":
    while True:
        url = input("\nEnter Url or Quit = q: ")
        if url.lower() == 'q':
            break
        analyze_stream(url)
