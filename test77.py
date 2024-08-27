import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import wikipedia
import pyjokes

# Initialize speech recognition and text-to-speech engines
listener = sr.Recognizer()
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

# Set user agent in Wikipedia library
wikipedia.set_lang('en')
wikipedia.set_user_agent('Python/3.12.4 (tushartiwari581@gmail.com)')  # Set your user agent here

def talk(text):
    """Convert text to speech."""
    engine.say(text)
    engine.runAndWait()

def take_command():
    """Listen to the user's voice and return the recognized command."""
    try:
        command = ''
        with sr.Microphone() as source:
            print('listening...')
            voice = listener.listen(source)
            command = listener.recognize_google(voice)
            command = command.lower()
    except sr.UnknownValueError:
        talk('Sorry, I did not catch that. Could you please repeat?')
        return ''
    except sr.RequestError:
        talk('Sorry, there is a problem with the speech recognition service.')
        return ''
    return command

def get_summary(page_name):
    """Fetch summary from Wikipedia."""
    try:
        summary = wikipedia.summary(page_name, sentences=1)
        return summary
    except wikipedia.exceptions.DisambiguationError as e:
        return f"Disambiguation Error: {e.options}"
    except wikipedia.exceptions.PageError:
        return "Page Error: The page does not exist."
    except Exception as e:
        return f"An error occurred: {str(e)}"

def run_trinity():
    """Main function to run the assistant."""
    command = take_command()
    if not command:
        return
    
    print(command)
    if 'play' in command:
        song = command.replace('play', '').strip()
        talk('playing ' + song)
        pywhatkit.playonyt(song)
    elif 'time' in command:
        time = datetime.datetime.now().strftime('%H:%M:%S')
        talk('Current time is ' + time)
    elif 'search for' in command or 'who is' in command:
        if 'search for' in command:
            person = command.split('search for')[-1].strip()
        else:
            person = command.split('who is')[-1].strip()
        
        info = get_summary(person)
        print(info)
        talk(info)
    elif 'joke' in command:
        talk(pyjokes.get_joke())
    elif 'what is your name' in command:
        talk('I am Trinity')
        print('I am Trinity')
    elif 'who are you' in command:
        talk('I am Trinity, an AI.')
    elif 'hello trinity' in command:
        talk('At your service, sir.')
    elif 'what' in command:
        talk('I will make your work easy.')
    else:
        talk('Please say the command again.')

# Main loop
while True:
    run_trinity()
