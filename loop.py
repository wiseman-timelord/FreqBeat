# loop.py

# Imports
import time
import av
import threading
import pygetwindow as gw
import keyboard

# Globals
keyboard_thread = None

# Custom exception to signal a return to the main menu
class ReturnToMenuException(Exception):
    pass

# Listen for keyboard input and add it to the queue
def keyboard_input_listener(key_queue, stop_event):
    while not stop_event.is_set():
        current_window = gw.getActiveWindow()
        if "StatStream" in current_window.title:  # Changed from "python" to "StatStream"
            key = keyboard.read_key(suppress=True)
            key_queue.put(key)
        time.sleep(0.1)

# Main loop for handling the audio stream
def main_loop(url, speed, get_stream_url, analyze_stream, key_queue, speeds):
    global keyboard_thread
    
    # Initialize stop_event as None
    stop_event = None
    
    try:
        # Fetch the stream URL using the provided function
        stream_url = get_stream_url(url)
        if not stream_url:
            print("Unable to extract stream URL.")
            return
        
        # Initialize the number of reconnect attempts
        reconnect_attempts = 0
        
        # Stop the existing thread if any
        if keyboard_thread is not None and stop_event is not None:
            stop_event.set()
            keyboard_thread.join()
        
        # Create an event to stop the thread
        stop_event = threading.Event()
        
        # Start a separate thread to listen for keyboard input
        keyboard_thread = threading.Thread(target=keyboard_input_listener, args=(key_queue, stop_event))
        keyboard_thread.daemon = True
        keyboard_thread.start()
        
        # Main loop for reconnect attempts
        while reconnect_attempts < 10:
            try:
                # Open the audio stream
                container = av.open(stream_url)
                audio_stream = next(s for s in container.streams if s.type == 'audio')
                sample_rate = audio_stream.sample_rate
                
                # Inner loop for audio stream processing
                while True:
                    # Check for keyboard input
                    if not key_queue.empty():
                        key = key_queue.get()
                        if key == 'q':  # Quit if 'q' is pressed
                            return
                        else:
                            raise ReturnToMenuException  # Raise exception to return to the main menu
                    
                    start_time = time.time()
                    
                    # Analyze the audio stream
                    analyze_stream(container, audio_stream, sample_rate, speed, speeds, stream_url, key_queue)
                    
                    # Calculate elapsed time and sleep duration
                    elapsed_time = time.time() - start_time
                    sleep_duration = max(1.0/speed - elapsed_time, 0)
                    
                    # Sleep for the remaining time to match the desired speed
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
        # Handle the custom exception to return to the main menu
        print("Returning to the main menu...")
        
        # Stop the keyboard thread
        if keyboard_thread is not None:
            stop_event.set()
            keyboard_thread.join()
        
        return