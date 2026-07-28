"""
Workflow module for research automation using LangGraph.
"""
from src.workflows.research_workflow import ResearchWorkflow
from src.workflows.state_manager import ResearchState, create_initial_state

__all__ = [
    "ResearchWorkflow",
    "ResearchState",
    "create_initial_state"
]