# PrathamAI – Personal Voice Assistant
**PrathamAI** is an AI-powered personal voice assistant built using Python. It combines speech recognition, text-to-speech, Google's Gemini AI, and a graphical user interface powered by Kivy to provide an interactive voice-controlled experience.
PrathamAI can perform everyday tasks, answer questions, retrieve information, and execute system commands through natural voice interactions.

Features

- **Voice Recognition:** Recognizes spoken commands using Google Speech Recognition.
- **AI-Powered Conversations:** Uses Google's Gemini 2.0 Flash model to generate intelligent responses.
- **Text-to-Speech:** Converts AI responses and assistant messages into speech.
- **Graphical User Interface:** Interactive GUI built with Kivy.
- **YouTube Integration:** Search and play videos on YouTube using voice commands.
- **Google Search:** Perform Google searches through voice commands.
- **Wikipedia Search:** Retrieve information from Wikipedia.
- **Email Automation:** Send emails using voice instructions.
- **Latest News:** Get the latest news headlines.
- **Weather Information:** Retrieve weather information for a specified city.
- **Movie Information:** Search movies and retrieve details such as release year, IMDb rating, cast, and plot.
- **System Automation:** Open applications such as Command Prompt, Notepad, Chrome, and Visual Studio Code.
- **IP Address Lookup:** Retrieve your public IP address.
- **Audio Visualization:** Displays microphone input volume through an animated interface.
- **Keyboard Shortcut:** Press the backtick (`) key to activate voice recording.

## Technologies Used

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| Kivy | Graphical user interface |
| Google Gemini API | AI-powered responses |
| SpeechRecognition | Speech-to-text |
| PyAudio | Microphone input |
| SoundDevice | Audio processing |
| NumPy | Numerical computations |
| pyttsx3 / Custom TTS | Text-to-speech functionality |
| IMDbPY | Movie information |
| Keyboard | Keyboard shortcuts |
| Threading | Background speech recognition |

Installation and Setup

1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/PrathamAI.git
```

2. Navigate to the Project Directory

```bash
cd PrathamAI
```

3. Create a Virtual Environment

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

4. Install Dependencies

```bash
pip install -r requirements.txt
```

5. Configure API Keys

Create or update `constants.py`:

```python
SCREEN_HEIGHT = 1080
SCREEN_WIDTH = 1920

GEMINI_API_KEY = "YOUR_GEMINI_API_KEY"
```

Get your Gemini API key from:

[https://aistudio.google.com/apikey](https://aistudio.google.com/apikey)

6. Run the Application

```bash
python main.py
```

Interface

PrathamAI features an interactive voice assistant interface with:

- Animated central assistant display.
- Microphone volume visualization.
- Digital clock.
- Voice command subtitles.
- Interactive recording button.

Security

- Keep your Gemini API key private.
- Do not commit passwords, API keys, or email credentials.
- Use a `.gitignore` file for sensitive configuration files.

Future Improvements

- Wake-word detection for hands-free activation.
- Offline speech recognition.
- Improved natural language understanding.
- More advanced desktop automation.
- Persistent conversation memory.
- Multi-language voice support.
- Better error handling and asynchronous processing.
- Modernized graphical interface.

Author

**Pratham Nayak**

Creator and Developer of PrathamAI.

## License

This project is open-source. You may use, modify, and distribute it according to the terms of the license you choose.

---

**If you like this project, consider giving it a star on GitHub!**

*Built with Python, AI, and a passion for automation.*
