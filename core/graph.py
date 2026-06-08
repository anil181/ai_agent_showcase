from typing import TypedDict
from langgraph.graph import StateGraph, START, END
from .models import AgentState
from .engine import AgentEngine

class GraphManager:
    def __init__(self):
        self.engine = AgentEngine()
        self.graph = StateGraph(AgentState)
        
        # Define nodes
        self.graph.add_node("drafting", self.drafting_node)
        self.graph.add_node("researching", self.researching_node)
        self.graph.add_node("refining", self.refining_node)

        # Build edges
        self.graph.add_edge(START, "drafting")
        self.graph.add_edge("drafting", "researching")
        self.graph.add_edge("researching", "refining")
        self.graph.add_edge("refining", END)

        self.graph = self.graph.compile()

    def drafting_node(self, state: AgentState):
        draft = self.engine.generate_draft(state["input"])
        return {"content": draft, "status": "drafted"}

    def researching_node(self, state: AgentState):
        research = self.engine.perform_research(state["content"])
        return {"research_notes": research, "status": "researched"}

    def refining_node(self, state: AgentState):
        # In a complex graph, you'd fetch specific parts of the state here
        final = self.engine.refine_output(state["content"], state["research_notes"])
        return {"content": final, "status": "complete"}

    def run(self, input_text: str):
        initial_state = {
            "input": input_text,
            "history": [],
            "content": "",
            "research_notes": "",
            "status": "starting"
        }
        return self.graph.invoke(initial_state)
