import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import asyncio
import pytest

from agent_system.agent import Agent, Session
from agent_system.planner import EchoPlanner, ToolPlanner
from agent_system.input import UserInput
from agent_system.tools import EchoTool

@pytest.mark.asyncio
async def test_echo_agent():
    planner = EchoPlanner()
    agent = Agent(planner)
    session = Session(session_id="t1")
    result = await agent.handle(session, UserInput(text="ping"))
    assert "Echo: ping" in result


@pytest.mark.asyncio
async def test_tool_agent():
    planner = ToolPlanner()
    agent = Agent(planner, tools=[EchoTool()])
    session = Session(session_id="t2")
    result = await agent.handle(session, UserInput(text="pong"))
    assert result == "pong"
