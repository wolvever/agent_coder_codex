import asyncio
from agent_system.agent import Agent
from agent_system.planner import EchoPlanner
from agent_system.scheduler import Scheduler

async def main():
    planner = EchoPlanner()
    agent = Agent(planner)
    scheduler = Scheduler()
    result = await scheduler.run_task(agent, session_id="demo", query="hello world")
    print("Result:", result)

if __name__ == "__main__":
    asyncio.run(main())
