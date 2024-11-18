Friday - Smart Assistant
Friday - Smart Assistant is a Python-based virtual assistant that helps automate everyday tasks. It can fetch weather updates, open applications, provide Wikipedia summaries, and perform various other tasks through voice or text commands. The assistant is powered by a user-friendly GUI designed using Tkinter.

Features
Time-Based Greetings: Provides personalized greetings based on the time of day.
Speech Recognition: Understands and processes voice commands via the speech_recognition library.
Text-to-Speech: Responds to queries using the pyttsx3 library for text-to-speech conversion.
Weather Updates: Retrieves current weather data for any city using the OpenWeatherMap API.
Wikipedia Summaries: Fetches concise information about a topic from Wikipedia.
Application Launcher: Opens applications or websites based on user commands.
Date and Time Information: Provides the current or relative dates and times.
GUI Interface: A Tkinter-based GUI for an interactive and user-friendly experience.

Installation
Prerequisites
Python 3.8 or later
Pip (Python package manager)
OpenWeatherMap API key
Required Libraries
Install the dependencies using the following command:

pip install pyttsx3 speechrecognition wikipedia requests  

Setup
Rename the File
Save the code as buffer.py.

Replace the OpenWeatherMap API Key
Update the weather_api_key variable in the script with your valid OpenWeatherMap API key.

Custom Application Paths
Update the custom_app_paths dictionary with the paths of applications you frequently use.

How to Run
Ensure the file is saved as buffer.py.
Run the script using:

python buffer.py  
The GUI will appear. Click Start Friday to start interacting with the assistant.
Commands
Examples of Supported Commands
Weather
"What is the weather in [city]?"
Wikipedia
"Search Wikipedia for [topic]"
"Who is [person]?"
Applications
"Open [application name]"
"Open [website name] in browser"
Date and Time
"What is the time?"
"What is the date tomorrow?"
Windows Settings
"Open display settings"
"Open network settings"
To exit, simply say "Exit" or "Stop".

Features in Detail
Weather Updates
Fetches real-time weather data, including temperature, humidity, and general conditions for a given city.
Wikipedia Integration
Provides brief and concise Wikipedia summaries for user queries.
Custom Application Handling
Opens specific applications or web pages based on command context.
Intuitive GUI
Built with Tkinter, the GUI offers buttons to start or exit the assistant seamlessly.
Limitations
Requires an active internet connection for weather and Wikipedia queries.
Speech recognition accuracy may vary depending on the environment.
Application paths must be configured manually in custom_app_paths for efficient usage.
Future Enhancements
Incorporate advanced natural language understanding using AI models.
Add support for multi-platform usage on macOS and Linux.
Integrate additional APIs for improved functionality.

License
This project is licensed under the MIT License. Feel free to use, modify, and distribute it as required.

Acknowledgments
Wikipedia API
OpenWeatherMap API
Python Libraries: pyttsx3, speechrecognition, requests
