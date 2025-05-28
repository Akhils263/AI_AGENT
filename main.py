from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from langchain.tools import tool
from langgraph.prebuilt.chat_agent_executor import create_tool_calling_executor
from dotenv import load_dotenv

load_dotenv()

@tool
def calculator(a: int, b: int, operation: str) -> float:
    if operation == "add":
        return a + b
    elif operation == "subtract":
        return a - b
    elif operation == "multiply":
        return a * b
    elif operation == "divide":
        if b == 0:
            return "Cannot divide by zero"
        return a / b
    else:
        return "Invalid operation"


def main():
    model = ChatOpenAI(temperature=0)
    tools = [calculator]
    agent_executor = create_tool_calling_executor(model, tools)

    print("Hello from project-1! I am your AI agent. Type 'quit' to exit or continue chatting.")

    while True:
        user_input = input("YOU: ").strip()
        if user_input.lower() == 'quit':
            break
        print("ASSISTANT: ",end="")
        for chunk in agent_executor.stream({"messages": [HumanMessage(content=user_input)]}):
            if "tool_response" in chunk:
                print(chunk["tool_response"], end="")
            elif "agent" in chunk and "messages" in chunk["agent"]:
                for message in chunk["agent"]["messages"]:
                    print(message.content, end="")
        print()


if __name__ == "__main__":
    main()
