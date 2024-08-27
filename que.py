import tkinter as tk
from tkinter import simpledialog, messagebox
import pyttsx3

class QuestionApp:
    def __init__(self, master, questions):
        self.master = master
        self.questions = questions
        self.responses = {}

        # Initialize the TTS engine
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 150)
        self.engine.setProperty('volume', 0.9)

        # Create the GUI
        self.master.title("Interactive Question Program")
        self.master.geometry("600x400")
        
        self.label = tk.Label(master, text="Welcome to the Interactive Question Program!",
                              wraplength=550, font=("Helvetica", 14))
        self.label.pack(pady=20)
        
        self.start_button = tk.Button(master, text="Start", font=("Arial", 12), bg="#4CAF50", fg="white",
                                      command=self.ask_questions)
        self.start_button.pack(pady=10)
        
        self.quit_button = tk.Button(master, text="Quit", font=("Arial", 12), bg="#F44336", fg="white",
                                     command=master.quit)
        self.quit_button.pack(pady=10)
        
        self.current_question_index = 0

    def speak(self, text):
        self.engine.say(text)
        self.engine.runAndWait()

    def ask_questions(self):
        if self.current_question_index < len(self.questions):
            question = self.questions[self.current_question_index]
            self.speak(question)
            response = simpledialog.askstring("Input", question, parent=self.master)
            if response is not None:
                self.responses[question] = response
                self.current_question_index += 1
                self.ask_questions()  # Continue to the next question
            else:
                messagebox.showwarning("Warning", "You must answer the question!")
        else:
            self.show_results()

    def show_results(self):
        results_message = "\nThank you for your responses!\n"
        for question, response in self.responses.items():
            results_message += f"{question} - {response}\n"
        
        # Display the results in a message box
        messagebox.showinfo("Responses", results_message)
        
        # Optionally save the results to a file
        with open('responses.txt', 'w') as file:
            file.write(results_message)
        
        # Reset for a new session if needed
        self.current_question_index = 0
        self.responses = {}

def main():
    questions = [
        # Personal Information
        "What is your full name?",
        "How old are you?",
        "What is your date of birth?",
        "What is your gender?",
        "Where were you born?",
        "What is your nationality?",
        "What languages do you speak?",
        "What is your marital status?",
        "Do you have any siblings?",
        "What is your highest educational qualification?",
        "What is your current occupation?",
        "What is your phone number?",
        "What is your email address?",
        "Where do you currently live?",
        "What is your mailing address?",
        
        # Preferences
        "What is your favorite color?",
        "What is your favorite food?",
        "What is your favorite drink?",
        "What is your favorite book?",
        "What is your favorite movie?",
        "What is your favorite TV show?",
        "What is your favorite song?",
        "What is your favorite music genre?",
        "What is your favorite animal?",
        "What is your favorite holiday destination?",
        "What is your favorite hobby?",
        "What is your favorite sport?",
        "What is your favorite season?",
        "What is your favorite subject in school?",
        "What is your favorite type of cuisine?",
        "What is your favorite ice cream flavor?",
        "What is your favorite dessert?",
        "What is your favorite clothing brand?",
        "What is your favorite shoe brand?",
        "What is your favorite app on your phone?",
        "What is your favorite social media platform?",
        
        # Opinions
        "What do you think about climate change?",
        "What is your opinion on social media?",
        "Do you think technology is beneficial or harmful to society?",
        "What are your thoughts on politics?",
        "What do you think about online education?",
        "What is your view on working from home?",
        "Do you believe in aliens?",
        "What is your opinion on space exploration?",
        "What are your thoughts on renewable energy?",
        "Do you think electric cars are the future?",
        "What do you think about cryptocurrency?",
        "What are your views on mental health awareness?",
        "What do you think about fast fashion?",
        "What are your thoughts on the current education system?",
        "Do you think artificial intelligence is a threat or an opportunity?",
        
        # Hypothetical Scenarios
        "If you could have any superpower, what would it be?",
        "If you could live anywhere in the world, where would it be?",
        "If you won a million dollars, what would you do with it?",
        "If you could time travel, would you go to the past or the future?",
        "If you could meet any historical figure, who would it be?",
        "If you were an animal, what animal would you be?",
        "If you could change one thing about the world, what would it be?",
        "If you were a character in a movie, who would you be?",
        "If you could invent anything, what would it be?",
        "If you could eliminate one food from existence, what would it be?",
        "If you were the president for a day, what would you do?",
        "If you had a magic wand, what would you wish for?",
        "If you could be a famous person for a day, who would you choose?",
        "If you could have dinner with anyone, living or dead, who would it be?",
        "If you could live in any time period, which would it be?",
        "If you were stranded on a desert island, what three items would you want?",
        
        # Life Goals
        "What is your biggest dream?",
        "What are your career goals?",
        "What personal goals do you have for this year?",
        "Where do you see yourself in 5 years?",
        "What skills do you want to learn?",
        "What languages do you want to learn?",
        "What places do you want to visit?",
        "What hobbies do you want to explore?",
        "What are your financial goals?",
        "What are your health and fitness goals?",
        "What projects do you want to complete?",
        "What relationships do you want to build?",
        "What books do you want to read?",
        "What volunteer work do you want to do?",
        "What business ideas do you have?",
        
        # Personal Experiences
        "What is the most memorable moment of your life?",
        "What is the biggest challenge you've overcome?",
        "What is the best decision you've ever made?",
        "What is the worst decision you've ever made?",
        "What is the most adventurous thing you've ever done?",
        "What is the most embarrassing moment of your life?",
        "What is the happiest moment of your life?",
        "What is the saddest moment of your life?",
        "What is the most rewarding experience you've had?",
        "What is the most difficult decision you've ever made?",
        "What is something you've always wanted to try?",
        "What is a talent you wish you had?",
        "What is a skill you're proud of?",
        "What is a hobby you've always wanted to pick up?",
        "What is a book that changed your life?",
        
        # Fun Questions
        "Do you have a hidden talent?",
        "What is your spirit animal?",
        "Do you believe in ghosts?",
        "What is the weirdest food you've ever tried?",
        "What is the most unusual thing in your wallet/purse right now?",
        "What is the last TV show you binged watched?",
        "If you could be any fictional character, who would you choose?",
        "What is the strangest dream you've ever had?",
        "If you could swap lives with someone for a day, who would it be?",
        "Do you have a guilty pleasure?",
        "What is your go-to karaoke song?",
        "What is your weirdest habit?",
        "What would you do if you were invisible for a day?",
        "What is the funniest joke you know?",
        "What is something you've always wanted to learn to cook?",
        
        # Miscellaneous
        "What is your favorite childhood memory?",
        "What is something you're passionate about?",
        "What is your favorite thing to do on a rainy day?",
        "What do you enjoy doing in your free time?",
        "What is your proudest accomplishment?",
        "What is the most interesting place you've visited?",
        "What do you like to do for fun?",
        "What is your morning routine like?",
        "What is your evening routine like?",
        "What is something you've always wanted to do but haven't done yet?",
        "What is a goal you're currently working towards?",
        "What is your biggest fear?",
        "What is something you're grateful for?",
        "What is something you're currently learning?",
        "What is your favorite way to relax?",
    ]


    root = tk.Tk()
    app = QuestionApp(root, questions)
    root.mainloop()

if __name__ == "__main__":
    main()
