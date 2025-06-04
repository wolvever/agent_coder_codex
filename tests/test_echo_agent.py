import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import asyncio
import pytest

from agent_system.agent import Agent, Session
from agent_system.planner import EchoPlanner

@pytest.mark.asyncio
async def test_echo_agent():
    planner = EchoPlanner()
    agent = Agent(planner)
    session = Session(session_id="t1")
    result = await agent.handle(session, "ping")
    assert "Echo: ping" in result
