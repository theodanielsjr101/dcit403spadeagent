import random
import datetime
import asyncio
from spade.agent import Agent
from spade.behaviour import PeriodicBehaviour


class DisasterEnvironment:
    """Simulated disaster environment"""

    def __init__(self):
        self.temperature = 25
        self.water_level = 10
        self.smoke = 5

    def update(self):
        
        self.temperature += random.randint(-2, 5)
        self.water_level += random.randint(0, 4)
        self.smoke += random.randint(0, 3)

    def get_data(self):
        return {
            "temperature": self.temperature,
            "water_level": self.water_level,
            "smoke": self.smoke
        }


class SensorAgent(Agent):

    class MonitorBehaviour(PeriodicBehaviour):

        async def run(self):

            
            self.agent.environment.update()

            data = self.agent.environment.get_data()

            
            severity = self.calculate_severity(data)

            
            time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            log = f"""
Time: {time}
Temperature: {data['temperature']} °C
Water Level: {data['water_level']} cm
Smoke Level: {data['smoke']} %
Damage Severity: {severity}
----------------------------
"""

            
            with open("event_log.txt", "a") as file:
                file.write(log)

            
            print(log)

        def calculate_severity(self, data):

            if (
                data["temperature"] > 45 or
                data["water_level"] > 60 or
                data["smoke"] > 70
            ):
                return "HIGH"

            elif (
                data["temperature"] > 35 or
                data["water_level"] > 40 or
                data["smoke"] > 40
            ):
                return "MEDIUM"

            else:
                return "LOW"

    async def setup(self):

        print("SensorAgent started...")

        self.environment = DisasterEnvironment()

        behaviour = self.MonitorBehaviour(period=5)  
        self.add_behaviour(behaviour)


async def main():

    agent = SensorAgent(
        "theodices@xmpp.jp",  
        "00009999theo$"           
    )

    await agent.start()

    print("Agent is running...")

    while True:
        await asyncio.sleep(1)


if __name__ == "__main__":
    asyncio.run(main())
