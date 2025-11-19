"""
Intelligence Substrate for ASI
A foundational framework for building advanced AI systems with distributed cognition.
"""

from .core import IntelligenceSubstrate, CognitiveModule
from .reasoning import ReasoningEngine
from .memory import MemorySystem
from .learning import LearningEngine
from .coordination import AgentCoordinator

__version__ = "0.1.0"
__all__ = [
    "IntelligenceSubstrate",
    "CognitiveModule",
    "ReasoningEngine",
    "MemorySystem",
    "LearningEngine",
    "AgentCoordinator",
]
