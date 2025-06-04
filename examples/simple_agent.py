import asyncio
from agent_system.agent import Agent
from agent_system.planner import EchoPlanner
from agent_system.scheduler import Scheduler
from agent_system.input import UserInput

async def main():
    planner = EchoPlanner()
    agent = Agent(planner)
    scheduler = Scheduler()
    result = await scheduler.run_task(
        agent,
        session_id="demo",
        user_input=UserInput(text="hello world"),
    )
    print("Result:", result)

if __name__ == "__main__":
    asyncio.run(main())
