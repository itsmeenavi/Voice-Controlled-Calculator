import speech_recognition as sr
import pyttsx3

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
        print("Listening for your command...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    try:
        command = recognizer.recognize_google(audio)
        print(f"You said: {command}")
        return command.lower()
    except sr.UnknownValueError:
        speak("Sorry, I did not understand that.")
        return ""
    except sr.RequestError:
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

    try:
        # Evaluate the mathematical expression
        result = eval(command)
        response = f"The result is {result}"
        print(response)
        speak(response)
    except Exception as e:
        print(f"Error: {e}")
        speak("Sorry, I could not perform that calculation.")

def main():
    speak("Hello! I am your voice-controlled calculator. How can I help you today?")
    while True:
        command = listen_command()
        if 'exit' in command or 'quit' in command or 'stop' in command:
            speak("Goodbye!")
            break
        parse_command(command)

if __name__ == "__main__":
    main()
