"""
Learning Engine Module

Provides learning, adaptation, and self-improvement capabilities.
"""

from typing import Any, Dict, List, Optional, Tuple
from dataclasses import dataclass, field
import time
from .core import CognitiveModule, Thought, CognitiveState


@dataclass
class LearningExample:
    """Represents a learning example"""
    input: Any
    output: Any
    feedback: Optional[float] = None
    timestamp: float = field(default_factory=time.time)


class LearningEngine(CognitiveModule):
    """
    Learning engine that adapts and improves through experience.
    
    Supports supervised, unsupervised, and reinforcement learning paradigms.
    """
    
    def __init__(self, name: str = "LearningEngine"):
        super().__init__(name)
        self.training_examples: List[LearningExample] = []
        self.learned_patterns: Dict[str, Any] = {}
        self.learning_rate = 0.1
        self.learning_mode = "supervised"
    
    def process(self, input_data: Any) -> Thought:
        """
        Process input through learning engine.
        
        Args:
            input_data: Data to learn from or apply learned patterns to
        
        Returns:
            Thought containing learning result
        """
        self.state = CognitiveState.LEARNING
        
        try:
            # Apply learned patterns or learn new patterns
            if self.learning_mode == "supervised":
                result = self._supervised_learning(input_data)
            elif self.learning_mode == "unsupervised":
                result = self._unsupervised_learning(input_data)
            elif self.learning_mode == "reinforcement":
                result = self._reinforcement_learning(input_data)
            else:
                result = {"input": input_data}
            
            thought = Thought(
                content=result,
                confidence=self._calculate_learning_confidence(),
                source_module=self.name,
                metadata={"learning_mode": self.learning_mode}
            )
            
            return thought
        finally:
            self.state = CognitiveState.IDLE
    
    def _supervised_learning(self, input_data: Any) -> Dict[str, Any]:
        """Supervised learning from labeled examples"""
        # Extract patterns from training examples
        patterns_found = []
        
        for example in self.training_examples:
            if self._similarity(input_data, example.input) > 0.7:
                patterns_found.append(example.output)
        
        return {
            "type": "supervised",
            "input": input_data,
            "predictions": patterns_found,
            "training_examples_used": len(patterns_found)
        }
    
    def _unsupervised_learning(self, input_data: Any) -> Dict[str, Any]:
        """Unsupervised learning - discover patterns"""
        # Simplified clustering/pattern discovery
        pattern_key = self._extract_pattern_key(input_data)
        
        if pattern_key not in self.learned_patterns:
            self.learned_patterns[pattern_key] = []
        
        self.learned_patterns[pattern_key].append(input_data)
        
        return {
            "type": "unsupervised",
            "input": input_data,
            "pattern_cluster": pattern_key,
            "cluster_size": len(self.learned_patterns[pattern_key])
        }
    
    def _reinforcement_learning(self, input_data: Any) -> Dict[str, Any]:
        """Reinforcement learning - learn from rewards"""
        # Simplified Q-learning approach
        state_action = str(input_data)
        
        if state_action not in self.learned_patterns:
            self.learned_patterns[state_action] = {
                "q_value": 0.0,
                "visit_count": 0
            }
        
        pattern = self.learned_patterns[state_action]
        pattern["visit_count"] += 1
        
        return {
            "type": "reinforcement",
            "input": input_data,
            "q_value": pattern["q_value"],
            "visit_count": pattern["visit_count"]
        }
    
    def _similarity(self, a: Any, b: Any) -> float:
        """Calculate similarity between two inputs"""
        # Simplified similarity measure
        str_a = str(a).lower()
        str_b = str(b).lower()
        
        if str_a == str_b:
            return 1.0
        
        # Simple word overlap
        words_a = set(str_a.split())
        words_b = set(str_b.split())
        
        if not words_a or not words_b:
            return 0.0
        
        overlap = len(words_a & words_b)
        total = len(words_a | words_b)
        
        return overlap / total if total > 0 else 0.0
    
    def _extract_pattern_key(self, data: Any) -> str:
        """Extract pattern key for clustering"""
        # Simplified pattern extraction
        data_str = str(data).lower()
        
        # Use first few words as pattern key
        words = data_str.split()[:3]
        return "_".join(words) if words else "default"
    
    def _calculate_learning_confidence(self) -> float:
        """Calculate confidence in learning"""
        if len(self.training_examples) > 10:
            return 0.8
        elif len(self.training_examples) > 5:
            return 0.6
        return 0.4
    
    def update(self, feedback: Dict[str, Any]) -> None:
        """Update learning engine based on feedback"""
        if "reward" in feedback and self.learning_mode == "reinforcement":
            # Update Q-values based on reward
            reward = feedback["reward"]
            if "state_action" in feedback:
                state_action = feedback["state_action"]
                if state_action in self.learned_patterns:
                    pattern = self.learned_patterns[state_action]
                    old_q = pattern["q_value"]
                    pattern["q_value"] = old_q + self.learning_rate * (reward - old_q)
        
        # Track performance
        if "accuracy" in feedback:
            self.performance_metrics["accuracy"] = feedback["accuracy"]
    
    def add_training_example(self, input: Any, output: Any, 
                           feedback: Optional[float] = None) -> None:
        """Add a training example"""
        example = LearningExample(
            input=input,
            output=output,
            feedback=feedback
        )
        self.training_examples.append(example)
    
    def set_learning_mode(self, mode: str) -> None:
        """Set learning mode"""
        if mode in ["supervised", "unsupervised", "reinforcement"]:
            self.learning_mode = mode
        else:
            raise ValueError(f"Unknown learning mode: {mode}")
    
    def set_learning_rate(self, rate: float) -> None:
        """Set learning rate"""
        if 0.0 <= rate <= 1.0:
            self.learning_rate = rate
        else:
            raise ValueError("Learning rate must be between 0 and 1")
    
    def get_learned_patterns(self) -> Dict[str, Any]:
        """Get all learned patterns"""
        return self.learned_patterns.copy()
    
    def get_training_examples(self) -> List[LearningExample]:
        """Get all training examples"""
        return self.training_examples.copy()
