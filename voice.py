def chatbot_response(user_input):
    user_input = user_input.lower()
    
    if 'hello' in user_input or 'hi' in user_input:
        return "Hello! How can I assist you today?"
    elif 'how are you' in user_input:
        return "I'm just a program, but I'm doing great! How about you?"
    elif 'what is your name' in user_input:
        return "I am a chatbot created by OpenAI. What can I call you?"
    elif 'bye' in user_input:
        return "Goodbye! Have a great day!"
    else:
        return "Sorry, I didn't understand that. Can you please rephrase?"

def chat():
    print("Chatbot: Hi! Type 'bye' to exit.")
    
    while True:
        user_input = input("You: ")
        if 'bye' in user_input.lower():
            print("Chatbot: Goodbye! Have a great day!")
            break
        response = chatbot_response(user_input)
        print("Chatbot:", response)

if __name__ == "__main__":
    chat()
