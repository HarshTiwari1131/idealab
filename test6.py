import speech_recognition as s

sr=s.Recognizer()

print("i am listening you")

with s.Microphone() as m:
    audio=sr.listen(m)
    query=sr.recognize_google(audio,language='eng-in')
    print(query)
