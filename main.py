from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from langchain.tools import tool
from langgraph.prebuilt.chat_agent_executor import create_tool_calling_executor
from dotenv import load_dotenv

load_dotenv()

@tool
def calculator(int a , int b):
    print("Enter two numbers:")
    a = int(input("Enter first number: "))
    b = int(input("Enter second number: "))
    print("Choose your operation:")
    print("1. Add\n2. Subtract\n3. Multiply\n4. Divide")
    choice = int(input("Enter your choice (1-4): "))
    match choice:
        case '1':
            return a+b
        case '2':
            return a-b
        case '3':
            return a*b 
        case '4':
            return a/b
        default:
            print("Error")

def main():
    model = ChatOpenAI(temperature=0)
    tools = []
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
