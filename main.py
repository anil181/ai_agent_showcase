import os
from dotenv import load_dotenv
from core.graph import GraphManager

load_dotenv()

def main():
    print("Welcome to the AI Agent Showcase!")
    user_input = input("What topic should the agent write about? ")
    
    manager = GraphManager()
    result = manager.run(user_input)
    
    print("\n" + "="*30)
    print("FINAL OUTPUT:")
    print(result["content"])
    print("="*30)
    
if __name__ == "__main__":
    main()
