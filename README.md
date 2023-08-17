# FreqBeat
Status: Beta - Still, tweaking & bugfixing.

## Description
`FreqBeat` is a comprehensive audio stream analyzer designed to provide real-time insights into audio stream data from a given URL. Beyond just format and frequency, it delves into volume levels and offers a dynamic user interface for interaction. With the capability to extract streaming URLs from playlist files and direct stream links, `FreqBeat` ensures users have a seamless experience while viewing the analysis results on a clear console interface.

## Features
- **Support for Multiple Formats**: Currently supports, `.m3u`, `.pls`, direct stream URLs.
- **Real-time Frequency Analysis**: Calculates and shows, the dominant, low, medium, high frequencies.
- **Volume Level Detection**: Analyzes and displays, volume levels, as, quiet, normal, loud.
- **Interactive Interface**: Main interface allows users to control speed, input new URLs, or exit.
- **Configuration Management**: Persistient speed settings through YAML configuration file.
- **Error Handling**: Incorporates error mechanisms to address issues for, stream fetching, etc.

## INTERFACE
Output looks like this...

```
   ___________                   __________               __
   \_   _____/_____   ____  _____\______   \ ____ _____ _/  |_
    |    __|\_  __ \_/ __ \/ ____/|    |  _/| __ |\__  \|    _\
    |    \   |  | \/\  ___/| |_| ||    |   \  ___/ / __ \|  |
    \__  /   |__|    \___ \ \__  ||______  /\___ \/____  /__|
       \/                \/    \_\       \/     \/     \/


                       Speed: 1/2, Chunk: 21KB

               Channels: 2, Bits: 16Bit, Rate: 44Khz
                  Quiet [ ], Normal [*], Loud [ ]
               Low: 76Hz, Med: 9646Hz, High: 16078Hz


                       Press any key for Menu

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
