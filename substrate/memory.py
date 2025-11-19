"""
Memory System Module

Provides short-term, long-term, and working memory capabilities.
"""

from typing import Any, Dict, List, Optional
from dataclasses import dataclass, field
import time
from .core import CognitiveModule, Thought, CognitiveState


@dataclass
class MemoryItem:
    """Represents a memory item"""
    content: Any
    timestamp: float = field(default_factory=time.time)
    access_count: int = 0
    importance: float = 0.5
    tags: List[str] = field(default_factory=list)
    
    def access(self) -> None:
        """Record memory access"""
        self.access_count += 1


class MemorySystem(CognitiveModule):
    """
    Memory system with multiple memory types.
    
    Implements short-term memory (STM), long-term memory (LTM),
    and working memory for active cognitive processing.
    """
    
    def __init__(self, name: str = "MemorySystem", 
                 stm_capacity: int = 7,
                 ltm_capacity: int = 1000):
        super().__init__(name)
        self.short_term_memory: List[MemoryItem] = []
        self.long_term_memory: List[MemoryItem] = []
        self.working_memory: Dict[str, Any] = {}
        self.stm_capacity = stm_capacity
        self.ltm_capacity = ltm_capacity
    
    def process(self, input_data: Any) -> Thought:
        """
        Process input through memory system.
        
        Args:
            input_data: Data to store or retrieve
        
        Returns:
            Thought containing memory operation result
        """
        self.state = CognitiveState.PROCESSING
        
        try:
            # Store in short-term memory
            memory_item = MemoryItem(content=input_data)
            self._store_stm(memory_item)
            
            # Check for similar memories
            similar = self._find_similar(input_data)
            
            thought = Thought(
                content={
                    "stored": input_data,
                    "similar_memories": similar
                },
                confidence=0.9,
                source_module=self.name,
                metadata={"memory_type": "short_term"}
            )
            
            return thought
        finally:
            self.state = CognitiveState.IDLE
    
    def _store_stm(self, item: MemoryItem) -> None:
        """Store item in short-term memory"""
        self.short_term_memory.append(item)
        
        # Enforce capacity limit
        if len(self.short_term_memory) > self.stm_capacity:
            # Move oldest to long-term if important enough
            oldest = self.short_term_memory.pop(0)
            if oldest.importance > 0.5:
                self._consolidate_to_ltm(oldest)
    
    def _consolidate_to_ltm(self, item: MemoryItem) -> None:
        """Consolidate item to long-term memory"""
        self.long_term_memory.append(item)
        
        # Enforce capacity limit
        if len(self.long_term_memory) > self.ltm_capacity:
            # Remove least important/accessed items
            self.long_term_memory.sort(
                key=lambda x: x.importance * x.access_count
            )
            self.long_term_memory.pop(0)
    
    def _find_similar(self, content: Any, limit: int = 5) -> List[Any]:
        """Find similar memories"""
        similar = []
        content_str = str(content).lower()
        
        # Search in both STM and LTM
        all_memories = self.short_term_memory + self.long_term_memory
        
        for item in all_memories:
            item_str = str(item.content).lower()
            if content_str in item_str or item_str in content_str:
                similar.append(item.content)
                item.access()  # Record access
                
                if len(similar) >= limit:
                    break
        
        return similar
    
    def store(self, content: Any, importance: float = 0.5, 
              tags: Optional[List[str]] = None) -> None:
        """Explicitly store content in memory"""
        item = MemoryItem(
            content=content,
            importance=importance,
            tags=tags or []
        )
        self._store_stm(item)
    
    def retrieve(self, query: Any, memory_type: str = "all") -> List[Any]:
        """Retrieve memories matching query"""
        results = []
        
        if memory_type in ["all", "short_term"]:
            results.extend(self._search_memory(self.short_term_memory, query))
        
        if memory_type in ["all", "long_term"]:
            results.extend(self._search_memory(self.long_term_memory, query))
        
        return results
    
    def _search_memory(self, memory_list: List[MemoryItem], 
                      query: Any) -> List[Any]:
        """Search a memory list"""
        results = []
        query_str = str(query).lower()
        
        for item in memory_list:
            if query_str in str(item.content).lower():
                results.append(item.content)
                item.access()
        
        return results
    
    def update(self, feedback: Dict[str, Any]) -> None:
        """Update memory system based on feedback"""
        if "reinforce" in feedback:
            # Increase importance of recent memories
            for item in self.short_term_memory[-3:]:
                item.importance = min(1.0, item.importance * 1.2)
    
    def get_stm_contents(self) -> List[Any]:
        """Get short-term memory contents"""
        return [item.content for item in self.short_term_memory]
    
    def get_ltm_contents(self) -> List[Any]:
        """Get long-term memory contents"""
        return [item.content for item in self.long_term_memory]
    
    def clear_stm(self) -> None:
        """Clear short-term memory"""
        self.short_term_memory.clear()
    
    def clear_ltm(self) -> None:
        """Clear long-term memory"""
        self.long_term_memory.clear()
