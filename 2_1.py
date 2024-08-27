import speech_recognition as sr
import webbrowser
import wolframalpha
import time
import os
import pyperclip
import wikipedia
import win32com.client as wincl
from datetime import datetime
import pafy
from bs4 import BeautifulSoup as bs
import requests
import sys

v = wincl.Dispatch("SAPI.SpVoice")
cl = wolframalpha.Client('YVH8AY-R8H93LQAJ2')
r = sr.Recognizer()
r.pause_threshold = 0.7
r.energy_threshold = 500
shell = wincl.Dispatch("WScript.Shell")

v.Speak('At your service Sir!')
print('At your service Sir!')

# List of commands
def print_command_list():
    commands = {
        'search for': 'Perform a Google search.',
        'search YouTube for': 'Search YouTube for a specific query.',
        'academic search': 'Perform a Google Scholar search.',
        'wiki results for': 'Get Wikipedia results for a query.',
        'read the copied text': 'Read the text from the clipboard.',
        'save the text': 'Save clipboard text to a file.',
        'bookmark this page': 'Bookmark the current page.',
        'video for': 'Search for a video on YouTube.',
        'what is the time': 'Get the current time.',
        'what is the date': 'Get today\'s date.',
        'silence please': 'Stop listening.',
        'resume listening': 'Resume listening.',
        'stop listening': 'Stop the assistant from listening.',
        'calculate': 'Perform a calculation using WolframAlpha.',
        'open calculator': 'Open the Calculator application.',
        'open paint': 'Open the Paint application.',
        'play': 'Play music using Windows Media Player.',
        'download song': 'Download a song from YouTube.',
        'download video': 'Download a video from YouTube.',
        'magnet link for': 'Get a magnet link for a query.',
        'keyword list': 'Get a list of available commands.'
    }
    
    command_text = 'Here is a list of things I can do:\n'
    for command, description in commands.items():
        command_text += f'{command}: {description}\n'
    
    print(command_text)
    v.Speak('Here is a list of things I can do.')
    v.Speak(command_text)

# Commands
google = 'search for'
youtube = 'search YouTube for'
acad = 'academic search'
wkp = 'wiki results for'
rdds = 'read the copied text'
t = 'what is the time'
d = 'what is the date'
say = 'say'
copy = 'copy the text'
sav = 'save the text'
bkmk = 'bookmark this page'
vid = 'video for'
wtis = 'what is'
wtar = 'what are'
whis = 'who is'
whws = 'who was'
when = 'when'
where = 'where'
how = 'how'
lsp = 'silence please'
lsc = 'resume listening'
stoplst = 'stop listening'
sc = 'deep search'
calc = 'calculate'
keywd = 'keyword list'
calculat = 'open calculator'
paint = 'open paint'
playmusic = 'play'
dlmusic = 'download song'
dlvideo = 'download video'
mgntlink = 'magnet link for'

while True:
    with sr.Microphone() as source:
        try:
            v.Speak("How can I help you today?")
            print("How can I help you today?")
            print("Waiting for your command")
            audio = r.listen(source, timeout=None)
            message = str(r.recognize_google(audio)).lower()
            print('You said: ' + message)
            
            if google in message:
                words = message.split()
                del words[0:2]
                st = ' '.join(words)
                print('Google results for: ' + str(st))
                url = 'https://google.com/search?q=' + st
                webbrowser.open(url)
                v.Speak('Google Results for: ' + str(st))
                
            elif mgntlink in message:
                words = message.split()
                del words[0:3]
                st = ' '.join(words)
                query = str(st)
                url = 'https://pirateproxy.mx/search/' + query + '/0/99/0'
                print("Searching......")
                source = requests.get(url).text
                soup = bs(source, 'lxml')
                results = soup.find_all('div', class_='detName')
                i = 1
                for r in results:
                    print(i, r.text)
                    i += 1
                print("Enter the Serial Number of the search item you like to download: ")
                v.Speak("Enter the Serial Number of the search item you like to download: ")
                choice = int(input())
                print("Fetching data.....")
                v.Speak("Fetching data.....")
                magnet_results = soup.find_all('a', title='Download this torrent using magnet')
                a = []
                for m in magnet_results:
                    a.append(m['href'])
                magnet_link = (a[choice - 1])
                print("Magnet Link of your selected choice has been fetched.")
                pyperclip.copy(magnet_link)
                v.Speak("Your magnet link is now in your clipboard.")
                
            elif acad in message:
                words = message.split()
                del words[0:2]
                st = ' '.join(words)
                print('Academic results for: ' + str(st))
                url = 'https://scholar.google.com/scholar?q=' + st
                webbrowser.open(url)
                v.Speak('Academic Results for: ' + str(st))
                
            elif wkp in message:
                try:
                    words = message.split()
                    del words[0:3]
                    st = ' '.join(words)
                    wkpres = wikipedia.summary(st, sentences=2)
                    try:
                        print('\n' + str(wkpres) + '\n')
                        v.Speak(wkpres)
                    except UnicodeEncodeError:
                        v.Speak("Sorry! Please try searching again")
                except wikipedia.exceptions.DisambiguationError as e:
                    print(e.options)
                    v.Speak("Too many results for this keyword. Please be more specific and retry")
                    continue
                except wikipedia.exceptions.PageError as e:
                    print("This page doesn't exist")
                    v.Speak("No results found for: " + str(st))
                    continue
                
            elif rdds in message:
                print('Reading your text')
                words = message.split()
                del words[0:4]
                v.Speak(pyperclip.paste())
                
            elif say in message:
                words = message.split()
                del words[0:1]
                st = ' '.join(words)
                print("Repeating the text: " + str(st))
                v.Speak('Alright, Saying..: ' + str(st))
                
            elif copy in message:
                words = message.split()
                del words[0:3]
                st = ' '.join(words)
                pyperclip.copy(st)
                print("The text " + str(st) + " is now copied to clipboard!")
                v.Speak('The text ..' + str(st) + ' is now in your clipboard... Happy Pasting!')
                
            elif youtube in message:
                words = message.split()
                del words[0:3]
                st = ' '.join(words)
                print("Searching for " + str(st) + " on YouTube")
                url = 'https://www.youtube.com/results?search_query=' + str(st)
                webbrowser.open(url)
                v.Speak('YouTube Search results for: ' + str(st))
                
            elif vid in message:
                words = message.split()
                del words[0:2]
                st = ' '.join(words)
                print("Searching for " + str(st) + " on YouTube")
                url = 'https://www.youtube.com/results?search_query=' + str(st)
                webbrowser.open(url)
                v.Speak('YouTube Search results for: ' + str(st))
                
            elif t in message:
                c = time.ctime()
                words = c.split()
                v.Speak("The time is: " + str(words[3]))
                
            elif d in message:
                c = time.ctime()
                words = c.split()
                v.Speak("Today, it is " + words[2] + words[1] + words[4])
                
            elif sc in message:
                try:
                    words = message.split()
                    del words[0:2]
                    st = ' '.join(words)
                    scq = cl.query(st)
                    sca = next(scq.results).text
                    print('The answer is: ' + str(sca))
                    url = 'https://www.wolframalpha.com/input/?i=' + str(st)
                    v.Speak('The answer is: ' + str(sca))
                except StopIteration:
                    print('Your question is ambiguous. Please try with another keyword!')
                    v.Speak('Your question is ambiguous. Please try with another keyword!')
                except Exception as e:
                    print(e)
                    v.Speak(e)
                else:
                    v.Speak("I'm always correct")
                
            elif calc in message:
                try:
                    words = message.split()
                    del words[0:1]
                    st = ' '.join(words)
                    scq = cl.query(st)
                    sca = next(scq.results).text
                    print('The answer is: ' + str(sca))
                    url = 'https://www.wolframalpha.com/input/?i=' + str(st)
                    v.Speak('The answer is: ' + str(sca))
                except StopIteration:
                    print('Your question is ambiguous. Please try with another keyword!')
                    v.Speak('Your question is ambiguous. Please try with another keyword!')
                except Exception as e:
                    print(e)
                    v.Speak(e)
                else:
                    v.Speak("I'm always correct")
                
            elif paint in message:
                os.system('mspaint')
                
            elif sav in message:
                print('Saving your text to file')
                with open('path to your text file', 'a') as f:
                    f.write(pyperclip.paste())
                    v.Speak('File is successfully saved')
                
            elif bkmk in message:
                shell.SendKeys("^d")
                v.Speak("Alright, Page Bookmarked!")
                
            elif calculat in message:
                os.system('calc')
                
            elif 'open' in message:
                words = message.split()
                del words[0:1]
                st = ' '.join(words)
                if 'telegram' in str(st):
                    print('Opening Telegram')
                    v.Speak('Opening Telegram')
                    os.startfile(r'''C:\Users\asus1\AppData\Roaming\Telegram Desktop\Telegram.exe''')
                elif 'Chrome' in str(st):
                    print('Opening Chrome')
                    v.Speak('Opening Chrome')
                    os.startfile(r'''C:\Program Files (x86)\Google\Chrome\Application\chrome.exe''')
                elif 'Opera' in str(st):
                    print('Opening Opera')
                    v.Speak('Opening Opera')
                    os.startfile(r'''C:\Program Files\Opera\launcher.exe''')
                
            elif playmusic in message:
                os.system('start wmplayer')
                v.Speak("Opening Windows Media Player")
                
            elif dlmusic in message:
                try:
                    words = message.split()
                    del words[0:3]
                    st = ' '.join(words)
                    video = pafy.new(st)
                    best = video.getbest(preftype="mp4")
                    best.download()
                    print('Downloading your song')
                    v.Speak('Downloading your song')
                except Exception as e:
                    print(e)
                    v.Speak("An error occurred while trying to download the song.")
                
            elif dlvideo in message:
                try:
                    words = message.split()
                    del words[0:3]
                    st = ' '.join(words)
                    video = pafy.new(st)
                    best = video.getbest(preftype="mp4")
                    best.download()
                    print('Downloading your video')
                    v.Speak('Downloading your video')
                except Exception as e:
                    print(e)
                    v.Speak("An error occurred while trying to download the video.")
                
            elif keywd in message:
                print_command_list()
                
            elif lsp in message:
                print("Silencing")
                v.Speak("Silencing")
                continue
                
            elif lsc in message:
                print("Resuming listening")
                v.Speak("Resuming listening")
                
            elif stoplst in message:
                print("Stopping listening")
                v.Speak("Stopping listening")
                break
                
            else:
                print('Sorry, I didn\'t understand that.')
                v.Speak('Sorry, I didn\'t understand that.')
                
        except sr.UnknownValueError:
            v.Speak("Sorry, I didn't get that. Please repeat.")
            continue
        except sr.RequestError:
            v.Speak("Sorry, there was an issue with the speech recognition service.")
            continue
        except Exception as e:
            print(e)
            v.Speak("An error occurred: " + str(e))
            continue
