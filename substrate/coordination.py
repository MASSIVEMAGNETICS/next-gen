"""
Agent Coordination Module

Provides multi-agent coordination and collaboration capabilities.
"""

from typing import Any, Dict, List, Optional, Callable
from dataclasses import dataclass, field
from enum import Enum
import time
from .core import CognitiveModule, Thought, CognitiveState


class AgentRole(Enum):
    """Roles that agents can take"""
    COORDINATOR = "coordinator"
    WORKER = "worker"
    SPECIALIST = "specialist"
    OBSERVER = "observer"


@dataclass
class Agent:
    """Represents an agent in the system"""
    id: str
    role: AgentRole
    capabilities: List[str] = field(default_factory=list)
    active: bool = True
    performance: float = 1.0


@dataclass
class Task:
    """Represents a task for agents"""
    id: str
    description: str
    requirements: List[str] = field(default_factory=list)
    assigned_to: Optional[str] = None
    completed: bool = False
    result: Optional[Any] = None


class AgentCoordinator(CognitiveModule):
    """
    Agent coordinator for managing multiple intelligent agents.
    
    Handles task assignment, agent communication, and collaborative
    problem-solving across multiple agents.
    """
    
    def __init__(self, name: str = "AgentCoordinator"):
        super().__init__(name)
        self.agents: Dict[str, Agent] = {}
        self.tasks: Dict[str, Task] = {}
        self.communication_log: List[Dict[str, Any]] = []
        self.coordination_strategy = "round_robin"
    
    def process(self, input_data: Any) -> Thought:
        """
        Process input through agent coordinator.
        
        Args:
            input_data: Coordination request or task
        
        Returns:
            Thought containing coordination result
        """
        self.state = CognitiveState.COORDINATING
        
        try:
            # Determine if this is a task assignment or query
            if isinstance(input_data, dict) and "task" in input_data:
                result = self._handle_task(input_data)
            else:
                result = self._coordinate_agents(input_data)
            
            thought = Thought(
                content=result,
                confidence=self._calculate_coordination_confidence(),
                source_module=self.name,
                metadata={"strategy": self.coordination_strategy}
            )
            
            return thought
        finally:
            self.state = CognitiveState.IDLE
    
    def _handle_task(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """Handle a new task"""
        task = Task(
            id=task_data.get("id", f"task_{len(self.tasks)}"),
            description=task_data.get("task", ""),
            requirements=task_data.get("requirements", [])
        )
        
        # Assign to best agent
        assigned_agent = self._assign_task(task)
        
        self.tasks[task.id] = task
        
        return {
            "task_id": task.id,
            "assigned_to": assigned_agent,
            "status": "assigned"
        }
    
    def _assign_task(self, task: Task) -> Optional[str]:
        """Assign task to best suited agent"""
        if not self.agents:
            return None
        
        if self.coordination_strategy == "round_robin":
            # Simple round-robin assignment
            active_agents = [a for a in self.agents.values() if a.active]
            if active_agents:
                agent = active_agents[len(self.tasks) % len(active_agents)]
                task.assigned_to = agent.id
                return agent.id
        
        elif self.coordination_strategy == "capability_match":
            # Match based on capabilities
            best_agent = None
            best_score = 0.0
            
            for agent in self.agents.values():
                if not agent.active:
                    continue
                
                # Calculate match score
                match_score = sum(
                    1 for req in task.requirements 
                    if req in agent.capabilities
                )
                
                if match_score > best_score:
                    best_score = match_score
                    best_agent = agent
            
            if best_agent:
                task.assigned_to = best_agent.id
                return best_agent.id
        
        return None
    
    def _coordinate_agents(self, input_data: Any) -> Dict[str, Any]:
        """Coordinate agents for collective intelligence"""
        # Broadcast to all active agents
        responses = []
        
        for agent in self.agents.values():
            if agent.active:
                # Simulate agent response
                response = {
                    "agent_id": agent.id,
                    "role": agent.role.value,
                    "response": f"Processing: {input_data}"
                }
                responses.append(response)
                
                # Log communication
                self.communication_log.append({
                    "timestamp": time.time(),
                    "from": "coordinator",
                    "to": agent.id,
                    "message": input_data
                })
        
        return {
            "input": input_data,
            "agents_contacted": len(responses),
            "responses": responses
        }
    
    def _calculate_coordination_confidence(self) -> float:
        """Calculate confidence in coordination"""
        if not self.agents:
            return 0.3
        
        active_count = sum(1 for a in self.agents.values() if a.active)
        return min(0.9, 0.5 + (active_count * 0.1))
    
    def update(self, feedback: Dict[str, Any]) -> None:
        """Update coordinator based on feedback"""
        if "agent_id" in feedback and "performance" in feedback:
            agent_id = feedback["agent_id"]
            if agent_id in self.agents:
                self.agents[agent_id].performance = feedback["performance"]
    
    def register_agent(self, agent_id: str, role: AgentRole, 
                      capabilities: Optional[List[str]] = None) -> None:
        """Register a new agent"""
        if agent_id in self.agents:
            raise ValueError(f"Agent {agent_id} already registered")
        
        agent = Agent(
            id=agent_id,
            role=role,
            capabilities=capabilities or []
        )
        self.agents[agent_id] = agent
    
    def unregister_agent(self, agent_id: str) -> None:
        """Unregister an agent"""
        if agent_id in self.agents:
            del self.agents[agent_id]
    
    def set_agent_active(self, agent_id: str, active: bool) -> None:
        """Set agent active status"""
        if agent_id in self.agents:
            self.agents[agent_id].active = active
    
    def get_agent(self, agent_id: str) -> Optional[Agent]:
        """Get agent by ID"""
        return self.agents.get(agent_id)
    
    def get_all_agents(self) -> List[Agent]:
        """Get all agents"""
        return list(self.agents.values())
    
    def get_active_agents(self) -> List[Agent]:
        """Get all active agents"""
        return [a for a in self.agents.values() if a.active]
    
    def set_coordination_strategy(self, strategy: str) -> None:
        """Set coordination strategy"""
        if strategy in ["round_robin", "capability_match"]:
            self.coordination_strategy = strategy
        else:
            raise ValueError(f"Unknown strategy: {strategy}")
    
    def complete_task(self, task_id: str, result: Any) -> None:
        """Mark a task as completed"""
        if task_id in self.tasks:
            task = self.tasks[task_id]
            task.completed = True
            task.result = result
    
    def get_task(self, task_id: str) -> Optional[Task]:
        """Get task by ID"""
        return self.tasks.get(task_id)
    
    def get_pending_tasks(self) -> List[Task]:
        """Get all pending tasks"""
        return [t for t in self.tasks.values() if not t.completed]
    
    def get_communication_log(self) -> List[Dict[str, Any]]:
        """Get communication log"""
        return self.communication_log.copy()
