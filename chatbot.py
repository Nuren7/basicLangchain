
import os

from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, SystemMessage

from agent import create_agent, run_agent

load_dotenv()


def main():
  
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        print("Error: Set the GROQ_API_KEY environment variable.")
        print("Add it to a .env file as GROQ_API_KEY=your-key-here")
        return

    agent = create_agent(api_key)
    messages = [
        SystemMessage(
            content=(
                "You are a helpful assistant. Use the available tools when they "
                "are useful, then explain the result clearly."
            )
        ),
    ]

    print("Simple LangChain Chatbot")
    print("Type 'exit', 'quit', or 'bye' to end the conversation.\n")

    while True:
  
        user_input = input("You: ")

        if user_input.lower() in ("exit", "quit", "bye"):
            print("Chatbot: Goodbye!")
            break
        messages.append(HumanMessage(content=user_input))
        answer = run_agent(messages, agent)
        print(f"Chatbot: {answer}")


if __name__ == "__main__":
    main()
