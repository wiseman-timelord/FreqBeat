# FreqBeat
Status: Pre-release  
A real-time audio stream analyzer designed to extract and display dominant frequencies.

## Description
`FreqBeat` is a Python-based tool tailored for analyzing audio streams from various sources. It calculates and displays the dominant frequency for both left and right audio channels in real-time. With support for multiple playlist formats and direct stream URLs, `FreqBeat` offers a clear console interface for users to interact with and view the analysis results.

## Features
- **Support for Multiple Formats**: Handles `.m3u`, `.pls`, and direct audio stream URLs.
- **Real-time Frequency Analysis**: Calculates and displays the dominant frequency for both left and right audio channels.
- **Continuous Analysis**: The tool continuously analyzes the audio stream and updates the displayed frequencies in real-time.
- **Clear Console Interface**: Provides a user-friendly interface that updates the displayed information in real-time.
- **Error Handling**: Built-in error handling for issues related to opening the stream or if the stream doesn't contain audio.

## INTERFACE
Output looks like this...

```

                    FreqBeat


      Chan: 2, Bits: 16Bit, Rate: 44Khz

            Left  Freq.: 306.25Hz
            Right Freq.: 306.25Hz

```

## Usage
1. Clone the repository or download the script.
2. Run the script using `python freqbeat.py`.
3. Enter the URL of the audio stream when prompted.
4. View the real-time analysis of the audio stream's dominant frequencies.
5. Enter a new URL or quit the program as needed.

## Requirements
- Python 3.7 or higher
- Internet connection
- URL linked to an audio stream

## Dependencies
- Python
- Windows (Optional).

## Disclaimer
"FreqBeat" is provided "as is," and the creators make no warranties regarding its use. Users are solely responsible for the content they analyze and any potential damages to their equipment. The use of "FreqBeat" for unauthorized activities is strictly at the user's own risk, and all legal responsibilities lie with the user.
