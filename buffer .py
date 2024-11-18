import tkinter as tk
from tkinter import messagebox
import pyttsx3
import speech_recognition as sr
import datetime
import wikipedia
import os
import subprocess
import webbrowser
import requests

# Initialize the speech engine
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)  # 0 for male, 1 for female

# Replace with your OpenWeatherMap API key
weather_api_key = "24c32e27fbb57b54b647045e13224202"

# Custom paths for some commonly used applications
custom_app_paths = {
    "notepad": "C:\\Windows\\system32\\notepad.exe",
    "calculator": "C:\\Windows\\system32\\calc.exe",
    "chrome": "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
}

def speak(text):
    engine.say(text)
    engine.runAndWait()

def wish_user():
    hour = datetime.datetime.now().hour
    if 0 <= hour < 12:
        speak("Good morning!")
    elif 12 <= hour < 18:
        speak("Good afternoon!")
    else:
        speak("Good evening!")
    speak("I am Friday. How can I assist you today?")

def take_command():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.pause_threshold = 1
        audio = recognizer.listen(source)
    try:
        print("Recognizing...")
        query = recognizer.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")
    except Exception as e:
        print("Could you please repeat that?")
        return None
    return query.lower()

def find_application_path(app_name):
    if app_name in custom_app_paths:
        path = custom_app_paths[app_name]
        if os.path.exists(path):
            return path
        else:
            return None

    try:
        subprocess.Popen([app_name])
        return None
    except FileNotFoundError:
        print(f"{app_name} not found in system PATH.")

    for root_dir in [os.getenv('ProgramFiles'), os.getenv('ProgramFiles(x86)')]:
        if root_dir:
            for dirpath, _, filenames in os.walk(root_dir):
                for filename in filenames:
                    if filename.lower() == f"{app_name}.exe":
                        path = os.path.join(dirpath, filename)
                        return path

    return None

def open_application(app_name):
    if "in browser" in app_name:
        website = app_name.replace("open", "").replace("in browser", "").strip()
        if website:
            speak(f"Opening {website} in the browser.")
            if not website.startswith("http"):
                website = "https://" + website
            webbrowser.open(website)
            return
        else:
            speak("Please provide a valid website name.")
            return

    if "settings" in app_name:
        speak("Opening Windows Settings.")
        os.system("start ms-settings:")
        return

    if "display" in app_name:
        speak("Opening Display Settings.")
        os.system("start ms-settings:display")
        return
    elif "network" in app_name:
        speak("Opening Network Settings.")
        os.system("start ms-settings:network")
        return
    elif "privacy" in app_name:
        speak("Opening Privacy Settings.")
        os.system("start ms-settings:privacy")
        return

    path = find_application_path(app_name)
    if path:
        speak(f"Opening {app_name}.")
        os.startfile(path)
    else:
        speak(f"Sorry, I can't find the application {app_name} on your system.")

def get_weather(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={weather_api_key}&units=metric"
    response = requests.get(url)
    data = response.json()

    if response.status_code == 200:
        main = data["main"]
        weather = data["weather"][0]["description"]
        temp = main["temp"]
        humidity = main["humidity"]
        return f"The weather in {city} is {weather} with a temperature of {temp} degrees Celsius and humidity of {humidity} percent."
    elif data.get("cod") == "404":
        return "I couldn't find the weather information for that location. Please check the city name and try again."
    else:
        return "I'm having trouble retrieving the weather information right now. Please try again later."

def get_relative_date(date_query):
    today = datetime.datetime.now()

    if "yesterday" in date_query:
        relative_date = today - datetime.timedelta(days=1)
    elif "tomorrow" in date_query:
        relative_date = today + datetime.timedelta(days=1)
    elif "next week" in date_query:
        relative_date = today + datetime.timedelta(weeks=1)
    elif "last week" in date_query:
        relative_date = today - datetime.timedelta(weeks=1)
    else:
        relative_date = today

    return relative_date.strftime("%A, %B %d, %Y")

def perform_task(query):
    if 'wikipedia' in query:
        speak("Searching Wikipedia...")
        query = query.replace("wikipedia", "")
        try:
            results = wikipedia.summary(query, sentences=2)
            speak("According to Wikipedia")
            speak(results)
        except wikipedia.exceptions.DisambiguationError as e:
            speak("There are multiple results for your query. Here are a few options:")
            for option in e.options[:5]:
                speak(option)
            speak("Please specify which one you meant by saying the name.")
            choice = take_command()
            if choice and choice.lower() in [option.lower() for option in e.options]:
                results = wikipedia.summary(choice, sentences=2)
                speak(f"According to Wikipedia, {choice}")
                speak(results)
            else:
                speak("Sorry, I couldn't find the option you specified.")

    elif 'open' in query:
        app_name = query.replace("open", "").strip()
        open_application(app_name)

    elif 'time' in query:
        str_time = datetime.datetime.now().strftime("%H:%M:%S")
        speak(f"The time is {str_time}")

    elif 'date' in query:
        date_info = get_relative_date(query)
        speak(f"The requested date is {date_info}")

    elif 'weather' in query:
        speak("For which city would you like to know the weather?")
        city = take_command()
        if city:
            weather_info = get_weather(city)
            speak(weather_info)

    elif 'who is' in query or 'tell me about' in query:
        person = query.replace("who is", "").replace("tell me about", "").strip()
        speak(f"Searching Wikipedia for {person}")
        results = wikipedia.summary(person, sentences=2)
        speak(results)

    else:
        speak("I didn't understand the command. Please try again.")

# GUI Setup with Tkinter
def start_gui():
    def on_start_button_click():
        wish_user()
        while True:
            query = take_command()
            if query:
                if 'exit' in query or 'stop' in query:
                    speak("Goodbye!")
                    break
                perform_task(query)

    root = tk.Tk()
    root.title("Friday Assistant")
    root.geometry("400x300")
    root.configure(bg="#2C3E50")

    label = tk.Label(root, text="Welcome to Friday Assistant", font=("Helvetica", 14, "bold"), fg="#ECF0F1", bg="#2C3E50")
    label.pack(pady=20)

    start_button = tk.Button(
        root,
        text="Start Friday",
        command=on_start_button_click,
        width=20,
        height=2,
        font=("Helvetica", 12, "bold"),
        fg="#2C3E50",
        bg="#E74C3C",
        activebackground="#C0392B",
        activeforeground="#ECF0F1",
        relief="raised",
        bd=5
    )
    start_button.pack(pady=20)

    exit_button = tk.Button(
        root,
        text="Exit",
        command=root.quit,
        width=20,
        height=2,
        font=("Helvetica", 12, "bold"),
        fg="#2C3E50",
        bg="#3498DB",
        activebackground="#2980B9",
        activeforeground="#ECF0F1",
        relief="raised",
        bd=5
    )
    exit_button.pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    start_gui()
