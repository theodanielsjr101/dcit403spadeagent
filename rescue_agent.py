# rescue_agent.py - Lab 3 version (complete)
import spade
from spade.agent import Agent
from spade.behaviour import FSMBehaviour, State
import asyncio
import datetime
import random

# -------- STATES --------

class MonitorState(State):
    async def run(self):
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        print(f"\n[{timestamp}] [RESCUE] 🔍 Monitoring for sensor reports...")
        
        # Check if sensor has reported an event
        # For Lab 3, we'll simulate receiving from sensor
        if hasattr(self.agent, 'sensor_trigger') and self.agent.sensor_trigger:
            severity, message = self.agent.sensor_trigger
            self.agent.current_event = (severity, message)
            self.agent.sensor_trigger = None  # Clear trigger
            print(f"[RESCUE] ⚠️ Event received from sensor: {message}")
            self.set_next_state("ASSESS")
        else:
            # Simulate sensor trigger randomly (for demo)
            if random.random() < 0.3:  # 30% chance
                from environment import generate_disaster_event
                self.agent.current_event = generate_disaster_event()
                print("[RESCUE] ⚠️ Event detected directly!")
                self.set_next_state("ASSESS")
            else:
                print("[RESCUE] No events, continuing monitoring")
                await asyncio.sleep(2)
                self.set_next_state("MONITOR")

class AssessState(State):
    async def run(self):
        severity, message = self.agent.current_event
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        
        print(f"[{timestamp}] [RESCUE] 📊 ASSESSING: {message}")
        print(f"[{timestamp}] [RESCUE] Severity: {severity}")
        
        # Define rescue goals based on severity
        if severity == "LOW":
            print("[RESCUE] ✅ Goal: No rescue required - continue monitoring")
            self.set_next_state("MONITOR")
            
        elif severity == "MEDIUM":
            print("[RESCUE] ⚠️ Goal: Deploy standard rescue team")
            self.agent.rescue_goal = "standard_rescue"
            self.set_next_state("RESCUE")
            
        else:  # HIGH
            print("[RESCUE] 🚨 Goal: Deploy emergency rescue team")
            self.agent.rescue_goal = "emergency_rescue"
            self.set_next_state("RESCUE")

class RescueState(State):
    async def run(self):
        severity, message = self.agent.current_event
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        goal = getattr(self.agent, 'rescue_goal', 'standard_rescue')
        
        print(f"[{timestamp}] [RESCUE] 🚑 EXECUTING: {goal}")
        
        # Simulate different rescue operations
        if goal == "emergency_rescue":
            print("[RESCUE] Deploying air support and medical teams...")
            await asyncio.sleep(3)
            print("[RESCUE] Evacuation in progress...")
        else:
            print("[RESCUE] Sending ground rescue team...")
            await asyncio.sleep(2)
            print("[RESCUE] Providing medical assistance...")
        
        # Store rescue outcome
        self.agent.rescue_outcome = {
            "severity": severity,
            "goal": goal,
            "completed": True,
            "time": timestamp
        }
        
        self.set_next_state("REPORT")

class ReportState(State):
    async def run(self):
        severity, message = self.agent.current_event
        outcome = self.agent.rescue_outcome
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        
        print(f"[{timestamp}] [RESCUE] 📝 REPORTING mission results")
        
        # Generate report
        report = f"""
╔════════════════════════════════════╗
║        RESCUE MISSION REPORT       ║
╠════════════════════════════════════╣
║ Time: {timestamp}         ║
║ Event: {message[:30]}...  ║
║ Severity: {severity}                    ║
║ Goal: {outcome['goal']}        ║
║ Status: COMPLETED                   ║
╚════════════════════════════════════╝
"""
        print(report)
        
        # Save to log
        with open("rescue_log.txt", "a") as f:
            f.write(f"[{timestamp}] MISSION: {severity} - {outcome['goal']}\n")
        
        # Return to monitoring
        await asyncio.sleep(1)
        self.set_next_state("MONITOR")

# -------- AGENT --------

class RescueAgent(Agent):
    async def setup(self):
        print("\n" + "="*50)
        print("RESCUE AGENT INITIALIZED")
        print("="*50)
        
        # Initialize attributes
        self.current_event = None
        self.rescue_goal = None
        self.rescue_outcome = None
        self.sensor_trigger = None  # Will receive from sensor
        
        # Create FSM
        fsm = FSMBehaviour()
        
        # Add states
        fsm.add_state(name="MONITOR", state=MonitorState(), initial=True)
        fsm.add_state(name="ASSESS", state=AssessState())
        fsm.add_state(name="RESCUE", state=RescueState())
        fsm.add_state(name="REPORT", state=ReportState())
        
        # Add transitions
        fsm.add_transition("MONITOR", "MONITOR")
        fsm.add_transition("MONITOR", "ASSESS")
        fsm.add_transition("ASSESS", "RESCUE")
        fsm.add_transition("ASSESS", "MONITOR")
        fsm.add_transition("RESCUE", "REPORT")
        fsm.add_transition("REPORT", "MONITOR")
        
        self.add_behaviour(fsm)
        print("[RESCUE] Ready for missions. Monitoring for events...\n")

# -------- MAIN --------

async def run_rescue_agent():
    """Run just the rescue agent (simplified for Lab 3)"""
    agent = RescueAgent(
        "theodices@xmpp.jp",
        "00009999theo$"
    )
    
    await agent.start(auto_register=True)
    print("Rescue Agent running. Press Ctrl+C to stop.\n")
    
    try:
        # Simulate sensor triggers occasionally
        while True:
            await asyncio.sleep(5)
            # Simulate sensor sending an event
            from environment import generate_disaster_event
            agent.sensor_trigger = generate_disaster_event()
            print("\n[MAIN] 📡 Simulated sensor trigger sent to rescue agent")
            
    except KeyboardInterrupt:
        print("\n\nStopping Rescue Agent...")
        await agent.stop()
        print("Agent stopped.")

if __name__ == "__main__":
    asyncio.run(run_rescue_agent())