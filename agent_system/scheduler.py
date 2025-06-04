import asyncio
from typing import Dict

from .agent import Agent, Session

class Scheduler:
    def __init__(self):
        self.sessions: Dict[str, Session] = {}

    def get_session(self, session_id: str) -> Session:
        if session_id not in self.sessions:
            self.sessions[session_id] = Session(session_id=session_id)
        return self.sessions[session_id]

    async def run_task(self, agent: Agent, session_id: str, query: str, instruction: str = "") -> str:
        session = self.get_session(session_id)
        result = await agent.handle(session, query, instruction)
        return result
