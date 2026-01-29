from spade.agent import Agent
from spade.behaviour import OneShotBehaviour
import asyncio

class HelloAgent(Agent):
    class GreetBehaviour(OneShotBehaviour):
        async def run(self):
            print("Hello from SPADE agent!")

    async def setup(self):
        self.add_behaviour(self.GreetBehaviour())

async def main():
    agent = HelloAgent("theodices@xmpp.jp", "00009999theo$")
    await agent.start()
    await asyncio.sleep(5)
    await agent.stop()

if __name__ == "__main__":
    asyncio.run(main())
