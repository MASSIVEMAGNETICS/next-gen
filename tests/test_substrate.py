"""
Tests for the Intelligence Substrate core components
"""

import unittest
from substrate import (
    IntelligenceSubstrate,
    CognitiveModule,
    ReasoningEngine,
    MemorySystem,
    LearningEngine,
    AgentCoordinator
)
from substrate.core import CognitiveState, Thought
from substrate.coordination import AgentRole


class TestIntelligenceSubstrate(unittest.TestCase):
    """Test the main IntelligenceSubstrate class"""
    
    def setUp(self):
        self.substrate = IntelligenceSubstrate(name="TestSubstrate")
    
    def test_initialization(self):
        """Test substrate initialization"""
        self.assertEqual(self.substrate.name, "TestSubstrate")
        self.assertEqual(self.substrate.global_state, CognitiveState.IDLE)
        self.assertEqual(len(self.substrate.modules), 0)
    
    def test_register_module(self):
        """Test registering a cognitive module"""
        reasoning = ReasoningEngine()
        self.substrate.register_module(reasoning)
        self.assertIn("ReasoningEngine", self.substrate.modules)
    
    def test_duplicate_module_registration(self):
        """Test that duplicate registration raises error"""
        reasoning = ReasoningEngine()
        self.substrate.register_module(reasoning)
        
        with self.assertRaises(ValueError):
            self.substrate.register_module(reasoning)
    
    def test_unregister_module(self):
        """Test unregistering a module"""
        reasoning = ReasoningEngine()
        self.substrate.register_module(reasoning)
        self.substrate.unregister_module("ReasoningEngine")
        self.assertNotIn("ReasoningEngine", self.substrate.modules)
    
    def test_context_management(self):
        """Test context setting and getting"""
        self.substrate.set_context("key1", "value1")
        self.assertEqual(self.substrate.get_context("key1"), "value1")
        self.assertIsNone(self.substrate.get_context("nonexistent"))
    
    def test_thought_stream(self):
        """Test thought stream management"""
        reasoning = ReasoningEngine()
        self.substrate.register_module(reasoning)
        
        thoughts = self.substrate.process_input("test input")
        self.assertGreater(len(thoughts), 0)
        self.assertGreater(len(self.substrate.get_thought_stream()), 0)
    
    def test_system_status(self):
        """Test getting system status"""
        status = self.substrate.get_system_status()
        self.assertIn("name", status)
        self.assertIn("state", status)
        self.assertIn("modules", status)


class TestReasoningEngine(unittest.TestCase):
    """Test the ReasoningEngine module"""
    
    def setUp(self):
        self.reasoning = ReasoningEngine()
    
    def test_initialization(self):
        """Test reasoning engine initialization"""
        self.assertEqual(self.reasoning.name, "ReasoningEngine")
        self.assertEqual(self.reasoning.reasoning_strategy, "deductive")
    
    def test_add_knowledge(self):
        """Test adding knowledge to the reasoning base"""
        self.reasoning.add_knowledge("Test knowledge")
        self.assertIn("Test knowledge", self.reasoning.knowledge_base)
    
    def test_set_strategy(self):
        """Test setting reasoning strategy"""
        self.reasoning.set_strategy("inductive")
        self.assertEqual(self.reasoning.reasoning_strategy, "inductive")
        
        with self.assertRaises(ValueError):
            self.reasoning.set_strategy("invalid_strategy")
    
    def test_process(self):
        """Test processing input"""
        thought = self.reasoning.process("test input")
        self.assertIsInstance(thought, Thought)
        self.assertIsNotNone(thought.content)
        self.assertEqual(thought.source_module, "ReasoningEngine")
    
    def test_deductive_reasoning(self):
        """Test deductive reasoning"""
        self.reasoning.add_knowledge("If A then B")
        self.reasoning.set_strategy("deductive")
        thought = self.reasoning.process("A")
        self.assertEqual(thought.content["type"], "deductive")


class TestMemorySystem(unittest.TestCase):
    """Test the MemorySystem module"""
    
    def setUp(self):
        self.memory = MemorySystem(stm_capacity=3, ltm_capacity=10)
    
    def test_initialization(self):
        """Test memory system initialization"""
        self.assertEqual(self.memory.name, "MemorySystem")
        self.assertEqual(self.memory.stm_capacity, 3)
        self.assertEqual(self.memory.ltm_capacity, 10)
    
    def test_store_and_retrieve(self):
        """Test storing and retrieving memories"""
        self.memory.store("Test memory")
        results = self.memory.retrieve("Test")
        self.assertIn("Test memory", results)
    
    def test_stm_capacity_limit(self):
        """Test short-term memory capacity limit"""
        for i in range(5):
            self.memory.store(f"Memory {i}", importance=0.3)
        
        # STM should not exceed capacity
        self.assertLessEqual(len(self.memory.short_term_memory), 3)
    
    def test_consolidation_to_ltm(self):
        """Test consolidation from STM to LTM"""
        for i in range(5):
            self.memory.store(f"Important memory {i}", importance=0.8)
        
        # Some memories should be in LTM
        self.assertGreater(len(self.memory.long_term_memory), 0)
    
    def test_clear_memory(self):
        """Test clearing memory"""
        self.memory.store("Test")
        self.memory.clear_stm()
        self.assertEqual(len(self.memory.short_term_memory), 0)


class TestLearningEngine(unittest.TestCase):
    """Test the LearningEngine module"""
    
    def setUp(self):
        self.learning = LearningEngine()
    
    def test_initialization(self):
        """Test learning engine initialization"""
        self.assertEqual(self.learning.name, "LearningEngine")
        self.assertEqual(self.learning.learning_mode, "supervised")
    
    def test_add_training_example(self):
        """Test adding training examples"""
        self.learning.add_training_example("input", "output")
        self.assertEqual(len(self.learning.training_examples), 1)
    
    def test_set_learning_mode(self):
        """Test setting learning mode"""
        self.learning.set_learning_mode("unsupervised")
        self.assertEqual(self.learning.learning_mode, "unsupervised")
        
        with self.assertRaises(ValueError):
            self.learning.set_learning_mode("invalid_mode")
    
    def test_set_learning_rate(self):
        """Test setting learning rate"""
        self.learning.set_learning_rate(0.05)
        self.assertEqual(self.learning.learning_rate, 0.05)
        
        with self.assertRaises(ValueError):
            self.learning.set_learning_rate(1.5)
    
    def test_process(self):
        """Test processing input"""
        thought = self.learning.process("test input")
        self.assertIsInstance(thought, Thought)
        self.assertEqual(thought.source_module, "LearningEngine")


class TestAgentCoordinator(unittest.TestCase):
    """Test the AgentCoordinator module"""
    
    def setUp(self):
        self.coordinator = AgentCoordinator()
    
    def test_initialization(self):
        """Test coordinator initialization"""
        self.assertEqual(self.coordinator.name, "AgentCoordinator")
        self.assertEqual(len(self.coordinator.agents), 0)
    
    def test_register_agent(self):
        """Test registering an agent"""
        self.coordinator.register_agent("agent_1", AgentRole.WORKER)
        self.assertIn("agent_1", self.coordinator.agents)
    
    def test_duplicate_agent_registration(self):
        """Test that duplicate registration raises error"""
        self.coordinator.register_agent("agent_1", AgentRole.WORKER)
        
        with self.assertRaises(ValueError):
            self.coordinator.register_agent("agent_1", AgentRole.WORKER)
    
    def test_unregister_agent(self):
        """Test unregistering an agent"""
        self.coordinator.register_agent("agent_1", AgentRole.WORKER)
        self.coordinator.unregister_agent("agent_1")
        self.assertNotIn("agent_1", self.coordinator.agents)
    
    def test_set_agent_active(self):
        """Test setting agent active status"""
        self.coordinator.register_agent("agent_1", AgentRole.WORKER)
        self.coordinator.set_agent_active("agent_1", False)
        agent = self.coordinator.get_agent("agent_1")
        self.assertFalse(agent.active)
    
    def test_task_assignment(self):
        """Test task assignment"""
        self.coordinator.register_agent("agent_1", AgentRole.WORKER, ["analysis"])
        
        thought = self.coordinator.process({
            "task": "Test task",
            "requirements": ["analysis"]
        })
        
        self.assertIn("task_id", thought.content)
        self.assertEqual(thought.content["status"], "assigned")
    
    def test_get_active_agents(self):
        """Test getting active agents"""
        self.coordinator.register_agent("agent_1", AgentRole.WORKER)
        self.coordinator.register_agent("agent_2", AgentRole.WORKER)
        self.coordinator.set_agent_active("agent_2", False)
        
        active = self.coordinator.get_active_agents()
        self.assertEqual(len(active), 1)


if __name__ == "__main__":
    unittest.main()
