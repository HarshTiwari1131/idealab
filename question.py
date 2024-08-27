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
        self.master.geometry("400x300")
        self.label = tk.Label(master, text="Welcome to the Interactive Question Program!", wraplength=350)
        self.label.pack(pady=20)
        
        self.start_button = tk.Button(master, text="Start", command=self.ask_questions)
        self.start_button.pack(pady=10)
        
        self.quit_button = tk.Button(master, text="Quit", command=master.quit)
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
        "What is your name?",
        "How old are you?",
        "What is your favorite color?",
        "Where do you live?",
        "What is your favorite food?",
        "What is your profession?"
    ]

    root = tk.Tk()
    app = QuestionApp(root, questions)
    root.mainloop()

if __name__ == "__main__":
    main()
