import speech_recognition as sr

# Initialize recognizer
recognizer = sr.Recognizer()

# Specify the correct device index
correct_device_index = 1  # Assuming this is the Microphone (Realtek(R) Audio)

try:
    # Use the microphone as the source
    with sr.Microphone(device_index=correct_device_index) as source:
        # Print available input devices for debugging
        print("Available input devices:")
        for i, device_name in enumerate(sr.Microphone.list_microphone_names()):
            print(f"Device {i}: {device_name}")

        print("Adjusting for ambient noise... Please wait.")
        # Adjust for ambient noise and set the minimum energy threshold
        recognizer.adjust_for_ambient_noise(source, duration=2)
        print(f"Set minimum energy threshold to {recognizer.energy_threshold}")

        print("Say something!")
        # Capture the audio
        audio = recognizer.listen(source, timeout=5)  # Timeout of 5 seconds

    try:
        # Recognize speech using Google Speech Recognition
        text = recognizer.recognize_google(audio, language='en-US')
        print("You said: " + text)
    except sr.UnknownValueError:
        print("Oops! Didn't catch that")
    except sr.RequestError as e:
        print("Could not request results; {0}".format(e))
except AssertionError as e:
    print(f"An error occurred: {e}")
    print("Please check the device index or permissions.")
except Exception as e:
    print(f"An unexpected error occurred: {e}")
