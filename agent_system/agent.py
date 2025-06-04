import asyncio
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional

from .events import Message, ToolUse, FinishAction
from .planner import Planner, PlanningContext, PlannerStep

@dataclass
class Session:
    session_id: str
    chat_history: List[Message] = field(default_factory=list)
    sandbox: Path = Path("./sandbox")

class Agent:
    def __init__(self, planner: Planner):
        self.planner = planner

    async def handle(self, session: Session, user_query: str, instruction: str = "") -> str:
        ctx = PlanningContext(
            session_id=session.session_id,
            user_query=user_query,
            chat_history=session.chat_history,
            tools=[],
            sandbox=session.sandbox,
            instruction=instruction,
        )
        while True:
            step = await self.planner.plan(ctx)
            session.chat_history.extend(step.messages)
            for msg in step.messages:
                print(f"{msg.role}: {msg.content}")
            for action in step.actions:
                if isinstance(action, FinishAction):
                    return action.result
            await asyncio.sleep(0)
