import speech_recognition as sr
import pyttsx3
import tkinter as tk
from tkinter import scrolledtext
import threading

# Initialize the recognizer and the text-to-speech engine
recognizer = sr.Recognizer()
tts_engine = pyttsx3.init()

def speak(text):
    """Convert text to speech."""
    tts_engine.say(text)
    tts_engine.runAndWait()

def listen_command():
    """Listen for a voice command and return it as text."""
    with sr.Microphone() as source:
        update_status("Listening for your command...")
        recognizer.adjust_for_ambient_noise(source)
        try:
            audio = recognizer.listen(source, timeout=5)
            command = recognizer.recognize_google(audio)
            update_command(f"You said: {command}")
            return command.lower()
        except sr.WaitTimeoutError:
            update_status("Listening timed out while waiting for phrase.")
            speak("I didn't hear anything. Please try again.")
            return ""
        except sr.UnknownValueError:
            update_status("Could not understand the audio.")
            speak("Sorry, I did not understand that.")
            return ""
        except sr.RequestError:
            update_status("Speech service is unavailable.")
            speak("Sorry, my speech service is down.")
            return ""

def parse_command(command):
    """Parse the voice command and perform calculation."""
    if not command:
        return

    # Supported operations
    operations = {
        'add': '+',
        'plus': '+',
        'subtract': '-',
        'minus': '-',
        'multiply': '*',
        'times': '*',
        'divide': '/',
        'divided by': '/'
    }

    # Replace words with operators
    for word, operator in operations.items():
        if word in command:
            command = command.replace(word, operator)

    # Remove any non-math words (like 'what is', 'calculate', etc.)
    # This can be enhanced with better NLP
    allowed_chars = "0123456789+-*/(). "
    command = ''.join(char for char in command if char in allowed_chars)

    try:
        # Evaluate the mathematical expression
        result = eval(command)
        response = f"The result is {result}"
        update_result(response)
        speak(response)
    except Exception as e:
        error_message = "Sorry, I could not perform that calculation."
        update_result(error_message)
        speak(error_message)

def process_command():
    """Process the voice command in a separate thread."""
    command = listen_command()
    parse_command(command)
    update_status("Ready.")

def start_listening():
    """Start listening in a new thread to avoid blocking the GUI."""
    threading.Thread(target=process_command, daemon=True).start()

def update_command(text):
    """Update the command display area."""
    command_display.config(state='normal')
    command_display.insert(tk.END, text + '\n')
    command_display.config(state='disabled')
    command_display.see(tk.END)

def update_result(text):
    """Update the result display area."""
    result_display.config(state='normal')
    result_display.insert(tk.END, text + '\n')
    result_display.config(state='disabled')
    result_display.see(tk.END)

def update_status(text):
    """Update the status label."""
    status_label.config(text=text)

def on_exit():
    """Handle the exit button."""
    speak("Goodbye!")
    root.destroy()

# Set up the Tkinter GUI
root = tk.Tk()
root.title("Voice-Controlled Calculator")
root.geometry("600x500")
root.resizable(False, False)

# Configure grid layout with padding
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

# Create a main frame
main_frame = tk.Frame(root, padx=10, pady=10)
main_frame.grid(row=0, column=0, sticky='nsew')

# Command display
command_label = tk.Label(main_frame, text="Commands:", font=("Helvetica", 12, "bold"))
command_label.grid(row=0, column=0, sticky='w')

command_display = scrolledtext.ScrolledText(main_frame, width=70, height=10, state='disabled', wrap=tk.WORD)
command_display.grid(row=1, column=0, pady=(0, 10))

# Result display
result_label = tk.Label(main_frame, text="Results:", font=("Helvetica", 12, "bold"))
result_label.grid(row=2, column=0, sticky='w')

result_display = scrolledtext.ScrolledText(main_frame, width=70, height=10, state='disabled', wrap=tk.WORD)
result_display.grid(row=3, column=0, pady=(0, 10))

# Status label
status_label = tk.Label(main_frame, text="Ready.", font=("Helvetica", 10, "italic"))
status_label.grid(row=4, column=0, pady=(0, 10), sticky='w')

# Buttons frame
buttons_frame = tk.Frame(main_frame)
buttons_frame.grid(row=5, column=0, pady=10)

# Listen Button
listen_button = tk.Button(buttons_frame, text="Listen", command=start_listening, width=12, bg="green", fg="white")
listen_button.grid(row=0, column=0, padx=10)

# Exit Button
exit_button = tk.Button(buttons_frame, text="Exit", command=on_exit, width=12, bg="red", fg="white")
exit_button.grid(row=0, column=1, padx=10)

# Initial greeting
def initial_greeting():
    speak("Hello! I am your voice-controlled calculator. Click the Listen button and tell me your command.")
    update_status("Ready.")

# Use `after` to ensure the greeting is spoken after the mainloop starts
root.after(100, initial_greeting)

root.mainloop()
