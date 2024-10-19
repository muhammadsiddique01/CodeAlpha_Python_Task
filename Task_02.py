import speech_recognition as sr
import webbrowser
import datetime
import os
import pyttsx3
import psutil  # For process management
import tkinter as tk  # For displaying time on screen

# Initialize the text-to-speech engine
engine = pyttsx3.init()

def speak(text):
    """Function to speak out the given text."""
    print(f"Sid: {text}")  # Print the text to console
    engine.say(text)  # Use text-to-speech engine to speak
    engine.runAndWait()  # Wait until speaking is finished

def take_command():
    """Function to take voice commands from the user."""
    recognizer = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source, duration=0.5)  # Adjust quickly for ambient noise
            print("Listening...")
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)  # Faster listening with timeout

        try:
            command = recognizer.recognize_google(audio)
            print(f"You said: {command}")  # Show what the user said in the terminal
            return command.lower()
        except sr.UnknownValueError:
            speak("Sorry, I did not understand that.")
            return None
        except sr.RequestError as e:
            speak("Sorry, there seems to be an issue with the speech recognition service.")
            return None

    except KeyboardInterrupt:
        print("Process interrupted by the user.")
        speak("Goodbye!")
        exit()

def greet_user():
    """Function to greet the user based on the time of day."""
    hour = datetime.datetime.now().hour
    if hour < 12:
        speak("Good morning!")
    elif 12 <= hour < 18:
        speak("Good afternoon!")
    else:
        speak("Good evening!")
    speak("I am your assistant Sid. How can I help you today?")

def open_google():
    """Function to open Google in the web browser."""
    webbrowser.open("https://www.google.com")
    speak("Google is now open. What would you like to search for?")

def search_google(query):
    """Function to perform a Google search."""
    webbrowser.open(f"https://www.google.com/search?q={query}")
    speak(f"Searching for {query} on Google.")

def close_google():
    """Function to close all Google browser windows and tabs by killing the process."""
    browser_processes = ['chrome', 'firefox', 'msedge']  # Supported browsers
    found = False  # To track if any browser process is found

    for proc in psutil.process_iter():
        for browser in browser_processes:
            if browser in proc.name().lower():
                proc.kill()  # Forcefully kill the process
                found = True

    if found:
        speak("All Google tabs and windows are now closed.")
    else:
        speak("No Google tabs or browsers were open.")

def open_notepad():
    """Function to open Notepad."""
    os.system("notepad")
    speak("Notepad is now close.")

def close_notepad():
    """Function to close Notepad by killing the process."""
    for proc in psutil.process_iter():
        if "notepad" in proc.name().lower():
            proc.kill()  # Kill Notepad process
            speak("Notepad is now closed.")
            return

def display_time():
    """Function to display the current time on the screen."""
    current_time = datetime.datetime.now().strftime("%H:%M:%S")

    global root  # Make root global so we can close it later
    root = tk.Tk()
    root.title("Current Time")
    root.geometry("400x200")
    root.attributes('-topmost', True)  # Keep the window above all others

    label = tk.Label(root, text=current_time, font=("Helvetica", 48))
    label.pack(expand=True)

    root.mainloop()  # Display the window

def close_time_display():
    """Function to close the time display window."""
    global root
    if root and root.winfo_exists():  # Check if window is still open
        root.destroy()
        speak("Time display closed.")
    else:
        speak("No time display was open.")

def main():
    greet_user()
    google_open = False  # Track if Google is open
    notepad_open = False  # Track if Notepad is open

    while True:
        user_command = take_command()
        if user_command is None:
            continue

        # Open Google and start the search loop
        if 'open google' in user_command:
            open_google()
            google_open = True

        # If Google is open, allow continuous search
        elif 'search' in user_command and google_open:
            search_query = user_command.replace('search', '').strip()
            if search_query:
                search_google(search_query)
            else:
                speak("What would you like to search for?")

        # Close the Google browser
        elif ('close google' in user_command or 'exit google' in user_command) and google_open:
            close_google()
            google_open = False

        # Open Notepad
        elif 'open notepad' in user_command:
            if not notepad_open:  # Check if Notepad is already open
                open_notepad()
                notepad_open = True

        # Close Notepad
        elif 'close notepad' in user_command:
            close_notepad()
            notepad_open = False

        # Check the time and display it on the screen
        elif 'time' in user_command:
            speak("Showing the current time on your screen.")
            display_time()

        # Close the time display window
        elif 'close time screen' in user_command:
            close_time_display()

        # Exit the entire assistant gracefully
        elif 'exit' in user_command:
            speak("Goodbye! Have a great day!")
            break  # Break the loop to end the assistant

        # Default response for unrecognized commands
        else:
            speak("I'm sorry, I can only perform Google searches, tell the time, open Notepad, or close apps.")

if __name__ == "__main__":
    main()
