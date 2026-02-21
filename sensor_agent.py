# sensor_agent.py - Lab 3 version (event trigger)
import random
import datetime
import asyncio
from spade.agent import Agent
from spade.behaviour import PeriodicBehaviour, FSMBehaviour, State
from environment import generate_disaster_event

class SensorFSMBehaviour(FSMBehaviour):
    async def on_start(self):
        print("[SENSOR] Sensor Agent FSM started")
    
    async def on_end(self):
        print("[SENSOR] Sensor Agent FSM finished")

class DetectState(State):
    """State 1: Detect environmental changes"""
    async def run(self):
        print("\n[SENSOR] 🌍 Detecting environmental conditions...")
        await asyncio.sleep(2)
        
        # Random chance to detect event (80% for demo purposes)
        if random.random() < 0.8:
            print("[SENSOR] ⚠️ Event detected! Moving to REPORT state")
            self.set_next_state("REPORT")
        else:
            print("[SENSOR] No significant changes, continuing detection")
            self.set_next_state("DETECT")

class ReportState(State):
    """State 2: Report event to rescue agent"""
    async def run(self):
        print("[SENSOR] 📡 Generating sensor report...")
        
        # Generate disaster event
        event = generate_disaster_event()
        severity, message = event
        
        # Store in agent
        self.agent.last_event = event
        self.agent.last_severity = severity
        
        # Log the sensor reading
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        log = f"[{timestamp}] SENSOR REPORT - Severity: {severity} - {message}"
        print(f"[SENSOR] {log}")
        
        with open("sensor_log.txt", "a") as f:
            f.write(log + "\n")
        
        # In Lab 4, this is where you'd send to rescue agent
        # For Lab 3, we'll just trigger the event in the same agent
        print(f"[SENSOR] Event triggered: {severity} severity")
        
        # Return to detection
        await asyncio.sleep(1)
        self.set_next_state("DETECT")

class SensorAgent(Agent):
    async def setup(self):
        print("\n" + "="*50)
        print("SENSOR AGENT INITIALIZED")
        print("="*50)
        
        self.last_event = None
        self.last_severity = None
        
        # Create FSM for sensor
        fsm = SensorFSMBehaviour()
        fsm.add_state(name="DETECT", state=DetectState(), initial=True)
        fsm.add_state(name="REPORT", state=ReportState())
        fsm.add_transition(source="DETECT", dest="DETECT")
        fsm.add_transition(source="DETECT", dest="REPORT")
        fsm.add_transition(source="REPORT", dest="DETECT")
        
        self.add_behaviour(fsm)
        print("[SENSOR] Monitoring for events...\n")