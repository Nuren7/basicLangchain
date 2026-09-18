
import os

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage


def main():
  
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("Error: Set the OPENAI_API_KEY environment variable.")
        print("Example: export OPENAI_API_KEY='your-key-here'")
        return

    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.7)
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
