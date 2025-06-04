import asyncio
from agent_system.agent import Agent
from agent_system.planner import EchoPlanner, ToolPlanner
from agent_system.scheduler import Scheduler
from agent_system.input import UserInput
from agent_system.tools import EchoTool

async def main(mode: str = "echo"):
    if mode == "use-tool":
        planner = ToolPlanner()
        agent = Agent(planner, tools=[EchoTool()])
    else:
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
    import sys
    mode = sys.argv[1] if len(sys.argv) > 1 else "echo"
    asyncio.run(main(mode))
