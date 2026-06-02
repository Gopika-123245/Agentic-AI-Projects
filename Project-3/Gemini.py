
import getpass
import os
from langchain_google_genai import ChatGoogleGenerativeAI

# Set up API key
if not os.environ.get("GOOGLE_API_KEY"):
    os.environ["GOOGLE_API_KEY"] = getpass.getpass("Enter API key for Google Gemini: ")

# Initialize model
model = ChatGoogleGenerativeAI(model="gemini-2.5-flash")

print("Chat started. Type 'exit' to stop.\n")

while True:
    user_input = input("You: ")

    if user_input.lower() in ["exit", "quit"]:
        print("Goodbye!")
        break

    response = model.invoke(user_input)
    print("Model:", response.content + "\n")
