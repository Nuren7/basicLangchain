
import os

from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_groq import ChatGroq


load_dotenv()


def main():
  
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        print("Error: Set the GROQ_API_KEY environment variable.")
        print("Add it to a .env file as GROQ_API_KEY=your-key-here")
        return

    llm = ChatGroq(
        model="llama-3.1-8b-instant",
        temperature=0.7,
        api_key=api_key,
    )
    messages = [
        SystemMessage(content="You are a helpful and friendly assistant."),
    ]

    print("Simple LangChain Chatbot")
    print("Type 'exit', 'quit', or 'bye' to end the conversation.\n")

    while True:
  
        user_input = input("You: ")

        if user_input.lower() in ("exit", "quit", "bye"):
            print("Chatbot: Goodbye!")
            break
        messages.append(HumanMessage(content=user_input))

        response = llm.invoke(messages)

        print(f"Chatbot: {response.content}")

        messages.append(AIMessage(content=response.content))


if __name__ == "__main__":
    main()
