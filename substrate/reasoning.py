"""
Reasoning Engine Module

Provides logical reasoning, inference, and decision-making capabilities.
"""

from typing import Any, Dict, List, Optional
from dataclasses import dataclass
from .core import CognitiveModule, Thought, CognitiveState


@dataclass
class Inference:
    """Represents a logical inference"""
    premise: Any
    conclusion: Any
    confidence: float
    reasoning_chain: List[str]


class ReasoningEngine(CognitiveModule):
    """
    Reasoning engine that performs logical inference and decision-making.
    
    Supports multiple reasoning strategies including deductive, inductive,
    and abductive reasoning.
    """
    
    def __init__(self, name: str = "ReasoningEngine"):
        super().__init__(name)
        self.knowledge_base: List[Any] = []
        self.inferences: List[Inference] = []
        self.reasoning_strategy = "deductive"
    
    def process(self, input_data: Any) -> Thought:
        """
        Process input through reasoning engine.
        
        Args:
            input_data: Data to reason about
        
        Returns:
            Thought containing reasoning result
        """
        self.state = CognitiveState.REASONING
        
        try:
            # Perform reasoning based on strategy
            if self.reasoning_strategy == "deductive":
                result = self._deductive_reasoning(input_data)
            elif self.reasoning_strategy == "inductive":
                result = self._inductive_reasoning(input_data)
            elif self.reasoning_strategy == "abductive":
                result = self._abductive_reasoning(input_data)
            else:
                result = {"raw": input_data}
            
            thought = Thought(
                content=result,
                confidence=self._calculate_confidence(result),
                source_module=self.name,
                metadata={"strategy": self.reasoning_strategy}
            )
            
            return thought
        finally:
            self.state = CognitiveState.IDLE
    
    def _deductive_reasoning(self, input_data: Any) -> Dict[str, Any]:
        """Apply deductive reasoning"""
        # Simplified deductive reasoning
        conclusions = []
        
        # Check against knowledge base
        for knowledge in self.knowledge_base:
            if self._matches_premise(input_data, knowledge):
                conclusions.append(knowledge)
        
        return {
            "type": "deductive",
            "input": input_data,
            "conclusions": conclusions
        }
    
    def _inductive_reasoning(self, input_data: Any) -> Dict[str, Any]:
        """Apply inductive reasoning"""
        # Simplified inductive reasoning - generalize from examples
        return {
            "type": "inductive",
            "input": input_data,
            "generalization": f"Pattern inferred from {input_data}"
        }
    
    def _abductive_reasoning(self, input_data: Any) -> Dict[str, Any]:
        """Apply abductive reasoning - inference to best explanation"""
        return {
            "type": "abductive",
            "input": input_data,
            "best_explanation": f"Most likely explanation for {input_data}"
        }
    
    def _matches_premise(self, input_data: Any, knowledge: Any) -> bool:
        """Check if input matches a knowledge premise"""
        # Simplified matching
        return str(input_data) in str(knowledge)
    
    def _calculate_confidence(self, result: Dict[str, Any]) -> float:
        """Calculate confidence in reasoning result"""
        # Simplified confidence calculation
        if "conclusions" in result and result["conclusions"]:
            return 0.8
        return 0.5
    
    def update(self, feedback: Dict[str, Any]) -> None:
        """Update reasoning engine based on feedback"""
        if "correct" in feedback:
            # Adjust confidence based on correctness
            if feedback["correct"]:
                self.performance_metrics["accuracy"] = \
                    self.performance_metrics.get("accuracy", 0.5) * 1.1
            else:
                self.performance_metrics["accuracy"] = \
                    self.performance_metrics.get("accuracy", 0.5) * 0.9
    
    def add_knowledge(self, knowledge: Any) -> None:
        """Add knowledge to the reasoning base"""
        self.knowledge_base.append(knowledge)
    
    def set_strategy(self, strategy: str) -> None:
        """Set reasoning strategy"""
        if strategy in ["deductive", "inductive", "abductive"]:
            self.reasoning_strategy = strategy
        else:
            raise ValueError(f"Unknown strategy: {strategy}")
    
    def get_inferences(self) -> List[Inference]:
        """Get all inferences made"""
        return self.inferences.copy()
