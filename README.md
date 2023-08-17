# FreqBeat
Status: Beta - Needs, tweaking & bugfixing.

## Description
`FreqBeat` is a comprehensive audio stream analyzer designed to provide real-time insights into audio stream data from a given URL. Beyond just format and frequency, it delves into volume levels and offers a dynamic user interface for interaction. With the capability to extract streaming URLs from playlist files and direct stream links, `FreqBeat` ensures users have a seamless experience while viewing the analysis results on a clear console interface.

## Features
- **Support for Multiple Formats**: Efficiently processes `.m3u`, `.pls`, and direct audio stream URLs.
- **Real-time Frequency Analysis**: Accurately calculates and showcases the dominant low, medium, and high frequencies for the audio stream.
- **Volume Level Detection**: Analyzes and displays volume levels, categorizing them as quiet, normal, or loud.
- **Continuous Analysis**: Ensures uninterrupted analysis of the audio stream, updating the results in real-time.
- **Interactive Console Interface**: Features a user-centric interface that not only displays the analysis but also allows users to control playback speed, input new URLs, or exit the program.
- **Keyboard Interactions**: Empowers users with keyboard shortcuts for functionalities like adjusting playback speed, changing the URL, or quitting the application.
- **Configuration Management**: Enables users to load and save configurations, primarily focusing on playback speed, from a YAML file.
- **Robust Error Handling**: Incorporates built-in error mechanisms to address potential issues related to stream fetching, decoding, or in scenarios where the stream lacks audio content.

## INTERFACE
Output looks like this...

```

                     FreqBeat

       Channels: 2, Bits: 16Bit, Rate: 44Khz
          Quiet [ ], Normal [ ], Loud [*]
      Low: 842Hz, Med: 7541Hz, High: 18489Hz

            Speed: 1/4s, Chunk: 10KB

```

## Usage
1. Clone the repository or download the script.
2. Run the script using `python freqbeat.py` or click `FreqBeat.bat`.
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
