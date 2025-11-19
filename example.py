"""
Example usage of the Intelligence Substrate for ASI

This example demonstrates how to use the intelligence substrate
to create a cognitive system with multiple modules working together.
"""

from substrate import (
    IntelligenceSubstrate,
    ReasoningEngine,
    MemorySystem,
    LearningEngine,
    AgentCoordinator
)
from substrate.coordination import AgentRole


def main():
    print("=" * 60)
    print("Intelligence Substrate for ASI - Example Usage")
    print("=" * 60)
    print()
    
    # Create the main intelligence substrate
    substrate = IntelligenceSubstrate(name="ASI-Demo")
    print(f"✓ Created substrate: {substrate.name}")
    print()
    
    # Create and register cognitive modules
    print("Registering cognitive modules...")
    
    # 1. Reasoning Engine
    reasoning = ReasoningEngine()
    reasoning.add_knowledge("If X then Y")
    reasoning.add_knowledge("Machine learning enables pattern recognition")
    substrate.register_module(reasoning)
    print(f"  ✓ Registered {reasoning.name}")
    
    # 2. Memory System
    memory = MemorySystem(stm_capacity=5, ltm_capacity=100)
    substrate.register_module(memory)
    print(f"  ✓ Registered {memory.name}")
    
    # 3. Learning Engine
    learning = LearningEngine()
    learning.add_training_example("hello", "greeting")
    learning.add_training_example("goodbye", "farewell")
    substrate.register_module(learning)
    print(f"  ✓ Registered {learning.name}")
    
    # 4. Agent Coordinator
    coordinator = AgentCoordinator()
    coordinator.register_agent("agent_1", AgentRole.WORKER, ["analysis", "reasoning"])
    coordinator.register_agent("agent_2", AgentRole.SPECIALIST, ["learning", "optimization"])
    substrate.register_module(coordinator)
    print(f"  ✓ Registered {coordinator.name}")
    print()
    
    # Demonstrate processing
    print("Processing examples...")
    print("-" * 60)
    
    # Example 1: Process through reasoning
    print("\n1. Reasoning about machine learning:")
    thoughts = substrate.process_input(
        "machine learning",
        target_module="ReasoningEngine"
    )
    for thought in thoughts:
        print(f"   Thought: {thought.content}")
        print(f"   Confidence: {thought.confidence:.2f}")
    
    # Example 2: Store and retrieve from memory
    print("\n2. Memory storage and retrieval:")
    memory.store("Artificial superintelligence requires robust reasoning", importance=0.9)
    memory.store("Neural networks are powerful learning tools", importance=0.8)
    retrieved = memory.retrieve("intelligence")
    print(f"   Retrieved {len(retrieved)} related memories:")
    for item in retrieved:
        print(f"     - {item}")
    
    # Example 3: Learning from examples
    print("\n3. Learning from patterns:")
    learning.set_learning_mode("unsupervised")
    thought = learning.process("hello world")
    print(f"   Learning result: {thought.content}")
    
    # Example 4: Multi-agent coordination
    print("\n4. Agent coordination:")
    task_result = coordinator.process({
        "task": "Analyze cognitive patterns",
        "requirements": ["analysis", "reasoning"]
    })
    print(f"   Task assignment: {task_result.content}")
    
    # Get system status
    print("\n" + "=" * 60)
    print("System Status:")
    print("-" * 60)
    status = substrate.get_system_status()
    print(f"Substrate: {status['name']}")
    print(f"State: {status['state']}")
    print(f"Thought stream size: {status['thought_stream_size']}")
    print(f"\nRegistered modules:")
    for module_name, module_info in status['modules'].items():
        print(f"  • {module_name}: {module_info['state']}")
    
    # Demonstrate thought stream
    print("\n" + "=" * 60)
    print("Recent Thought Stream:")
    print("-" * 60)
    recent_thoughts = substrate.get_thought_stream(limit=5)
    for i, thought in enumerate(recent_thoughts, 1):
        print(f"\n{i}. From: {thought.source_module}")
        print(f"   Content: {thought.content}")
        print(f"   Confidence: {thought.confidence:.2f}")
    
    print("\n" + "=" * 60)
    print("Intelligence Substrate Demo Complete!")
    print("=" * 60)


if __name__ == "__main__":
    main()
