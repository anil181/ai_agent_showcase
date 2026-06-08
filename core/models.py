from typing import Annotated, List, TypedDict
from typing_extensions import Literal

class AgentState(TypedDict):
    # The input query from the user
    input: str
    # The current status of the generation (e.g., "drafting", "researching", "refining")
    status: str
    # List of thoughts or steps taken
    history: List[str]
    # The research notes gathered during the research phase
    research_notes: str
    # The final content produced
    content: str
