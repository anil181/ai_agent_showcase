from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, SystemMessage
from typing import List

class AgentEngine:
    """
    A class-based wrapper for LangChain components to ensure
    more modular logic and easier testing of the core LLM interactions.
    """
    def __init__(self, model_name: str = "gemma4:12b"):
        # Using ChatOllama to connect to your local Ollama instance
        self.llm = ChatOllama(model=model_name, temperature=0.7)

    def generate_draft(self, topic: str) -> str:
        print(f"--- Generating draft for: {topic} ---")
        prompt = f"Write a brief outline and initial draft for the topic: {topic}"
        response = self.llm.invoke([SystemMessage(content="You are a creative writer."),
                                     HumanMessage(content=prompt)])
        return response.content

    def perform_research(self, current_content: str) -> str:
        print("--- Performing research phase ---")
        # In a real app, this would call search tools or browsing APIs.
        prompt = f"Analyze the following content and provide 3 additional facts or contextual nuances to improve it: {current_content}"
        response = self.llm.invoke([HumanMessage(content=prompt)])
        return response.content

    def refine_output(self, draft: str, research_notes: str) -> str:
        print("--- Refining final output ---")
        prompt = f"Combine the original draft and these research notes into a polished, professional article. Draft: {draft} Research: {research_notes}"
        response = self.llm.invoke([HumanMessage(content=prompt)])
        return response.content
