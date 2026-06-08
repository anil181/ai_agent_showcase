import os
from typing import List
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, SystemMessage
from tavily import TavilyClient

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

    def perform_research(self, current_content: str, topic: str = None) -> str:
        print("--- Performing research phase ---")
        
        # 1. Generate a search query based on the topic and current content
        if topic:
            query_prompt = f"Given the topic '{topic}' and the draft outline below, generate a single, concise search query to find additional facts and information on the internet. Return ONLY the search query string, with no quotes or extra text.\n\nDraft:\n{current_content}"
        else:
            query_prompt = f"Given the draft outline below, generate a single, concise search query to find additional facts and information on the internet. Return ONLY the search query string, with no quotes or extra text.\n\nDraft:\n{current_content}"
            
        query_response = self.llm.invoke([HumanMessage(content=query_prompt)])
        search_query = query_response.content.strip().strip('"').strip("'")
        print(f"Generated search query: '{search_query}'")
        
        # 2. Query Tavily Search API
        tavily_api_key = os.getenv("TAVILY_API_KEY")
        if not tavily_api_key or tavily_api_key == "your_tavily_api_key_here":
            raise ValueError("TAVILY_API_KEY environment variable is not set. Please add it to your .env file or environment.")
            
        tavily_client = TavilyClient(api_key=tavily_api_key)
        print(f"Searching Tavily for: '{search_query}'...")
        try:
            search_result = tavily_client.search(query=search_query, max_results=3)
        except Exception as e:
            print(f"Error querying Tavily: {e}")
            return f"Failed to perform research due to Tavily Search error: {e}"
            
        # 3. Format search results
        results_summary = ""
        for i, result in enumerate(search_result.get("results", [])):
            results_summary += f"\nSource {i+1}: {result.get('title', 'No Title')}\nURL: {result.get('url', 'No URL')}\nContent: {result.get('content', '')}\n"
            
        print("Fetched search results. Synthesizing research notes...")
        
        # 4. Generate 3 additional facts/nuances using the LLM and search results
        research_prompt = f"""You are a research assistant. Analyze the following draft and the internet search results below.
Provide 3 additional facts or contextual nuances, with references/citations to the sources, to improve the draft.

Draft:
{current_content}

Search Results:
{results_summary}
"""
        response = self.llm.invoke([HumanMessage(content=research_prompt)])
        return response.content

    def refine_output(self, draft: str, research_notes: str) -> str:
        print("--- Refining final output ---")
        prompt = f"Combine the original draft and these research notes into a polished, professional article. Draft: {draft} Research: {research_notes}"
        response = self.llm.invoke([HumanMessage(content=prompt)])
        return response.content
