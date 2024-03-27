# Voice Assistant App

This is a voice assistant application that listens for voice commands, transcribes the audio using Whisper, and executes various actions based on the transcribed text. The app uses a browser automation class to interact with the OpenAI GPT-4 model for generating responses to user prompts.

## Features

- Listens for voice commands continuously
- Transcribes audio using the Whisper model
- Executes external commands based on the transcribed text
- Interacts with the OpenAI GPT-4 model for generating responses
- Displays the generated responses in a popup window

## Installation

1. Clone the repository:
   ```git clone https://github.com/luishacm/voice-assistant-app.git```

2. Install the required dependencies:
   ```pip install -r requirements.txt```

3. Set up the necessary configurations:
   - Set the `profile_path` variable in `browser.py` to the path of your Selenium profile directory.
   - Adjust the `seconds_to_command` and `silence_threshold` variables in `app.py` according to your preferences.

4. Run the application:
   ```python app.py```

## Usage

1. Launch the application by running `app.py`.
2. The app will start listening for voice commands.
3. Speak a command that includes the keyword "luma" to activate the voice assistant.
4. The app will transcribe the audio and execute the corresponding action based on the transcribed text.
5. If the command requires interaction with the OpenAI GPT-4 model, the app will send the prompt to the model and display the generated response in a popup window.
6. To stop the application, say a command that includes the keyword "desligar" or "luma".

## File Structure

- `app.py`: The main entry point of the application. It handles audio recording, transcription, and command execution.
- `browser.py`: Contains the `Browser` class responsible for browser automation and interaction with the OpenAI GPT-4 model.
- `external_commands.py`: Defines the `ExternalCommands` class, which contains methods for executing various external commands based on the transcribed text.
- `popup_window.py`: Implements the popup window functionality for displaying the generated responses.

## Dependencies

- `faster_whisper`: Whisper model for audio transcription
- `sounddevice`: Audio input/output library
- `soundfile`: Audio file I/O library
- `numpy`: Numerical computing library
- `winsound`: Windows-specific sound playback library
- `selenium`: Browser automation library
- `undetected_chromedriver`: Undetected Chrome WebDriver for Selenium
- `psutil`: Process and system monitoring library
- `pygetwindow`: Library for retrieving window information
- `pyautogui`: GUI automation library
- `tkinter`: Standard Python GUI library

## Contributing

Contributions are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request.

## License

This project is licensed under the [MIT License](license).
