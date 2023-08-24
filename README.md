# StatStream
Status: Alpha, not progressing past "onset" or something similar, to then be in main loop with analysis displayed. Leaving project for a bit, mostly implemented & correct, will revisit later...

## Description
`StatStream` is an advanced audio stream analyzer that provides real-time insights into audio stream data. It supports a variety of audio formats and offers detailed analysis including frequency, volume, and tempo. The program also features a dynamic ASCII art console interface for enhanced user interaction.

## Features
- **Support for Multiple Protocols and Formats**: Supports `.m3u`, `.pls`, `.mp3`, `.aac`, `.ogg`, `.flac`, as well as `rtsp` and `mms` protocols.
- **Real-time Frequency and Volume Analysis**: Calculates and displays dominant low, medium, and high frequencies, as well as volume levels categorized as quiet, normal, and loud.
- **Tempo Analysis**: Provides real-time Beats Per Minute (BPM) analysis.
- **Interactive Interface**: Allows users to control speed, input new URLs, or exit the program. Also supports keyboard input for additional controls.
- **Configuration Management**: Persistent speed settings managed through a YAML configuration file.
- **Robust Error Handling**: Comprehensive error handling for issues like stream fetching, timeouts, and more.


## INTERFACE
Output looks like this...

```
     _________ __          __   _________ __                                 
    /   _____//  |______ _/  |_/   _____//  |________   ____ _____    _____  
    \_____  \\   __\__  \\   __\_____  \\   __\_  __ \_/ __ \\__  \  /     \ 
    /        \|  |  / __ \|  | /        \|  |  |  | \/\  ___/ / __ \|  Y Y  \
   /_______  /|__| |____  /__|/_______  /|__|  |__|    \___ \|____  /__|_|  /
           \/           \/            \/                   \/     \/      \/ 


                               Speed: 1/2, Chunk: 21KB

                       Channels: 2, Bits: 16Bit, Rate: 44Khz
                          Quiet [ ], Normal [*], Loud [ ]
                            BPM: 145, BPM Range: 122-166
                       Low: 76Hz, Med: 9646Hz, High: 16078Hz


                               Press any key for Menu

```


## Usage
1. Clone the repository or download the script.
2. Run the script using `python StatStream.py` or click `StatStream.bat`.
3. Enter the URL of the audio stream when prompted.
4. View the real-time analysis of the audio stream's dominant frequencies.
5. Press any key to return to Main Menu.


## Requirements
- Python 3.7 or higher
- Internet connection
- URL linked to an audio stream

## Dependencies
- Python
- Windows (Optional).

## Disclaimer
"StatStream" is provided "as is," and the creators make no warranties regarding its use. Users are solely responsible for the content they analyze and any potential damages to their equipment. The use of "StatStream" for unauthorized activities is strictly at the user's own risk, and all legal responsibilities lie with the user.
