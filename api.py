import openai
import os

# Load API key from environment variable
openai.api_key = os.getenv('OPENAI_API_KEY')

# Function to generate a response using OpenAI's GPT-4
def generate_response(prompt, conversation_history=None):
    if conversation_history is None:
        conversation_history = []

    conversation_history.append({"role": "user", "content": prompt})

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",  # Use the appropriate model here
            messages=conversation_history,
            max_tokens=150,
            n=1,
            stop=None,
            temperature=0.7
        )

        assistant_reply = response['choices'][0]['message']['content'].strip()
        conversation_history.append({"role": "assistant", "content": assistant_reply})

        return assistant_reply, conversation_history

    except Exception as e:
        return f"An error occurred: {e}", conversation_history

# Interactive loop
def main():
    print("AI Assistant: Hello! How can I assist you today?")
    conversation_history = [{"role": "system", "content": "You are a helpful assistant."}]

    while True:
        user_input = input("You: ")

        if user_input.lower() in ["exit", "quit"]:
            print("AI Assistant: Goodbye!")
            break

        response, conversation_history = generate_response(user_input, conversation_history)
        print(f"AI Assistant: {response}")

if __name__ == "__main__":
    main()
