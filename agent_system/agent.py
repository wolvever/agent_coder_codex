import asyncio
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional

from .events import Message, ToolUse, FinishAction
from .planner import Planner, PlanningContext, PlannerStep
from .sandbox import Sandbox
from .tools import Tool
from .input import UserInput

@dataclass
class Session:
    session_id: str
    chat_history: List[Message] = field(default_factory=list)
    sandbox: Sandbox = field(default_factory=lambda: Sandbox(Path("./sandbox")))

class Agent:
    def __init__(self, planner: Planner, tools: Optional[List[Tool]] = None):
        self.planner = planner
        self.tools = tools or []

    def _find_tool(self, name: str) -> Optional[Tool]:
        for tool in self.tools:
            if tool.name == name:
                return tool
        return None

    async def handle(self, session: Session, user_input: UserInput, instruction: str = "") -> str:
        ctx = PlanningContext(
            session_id=session.session_id,
            user_input=user_input,
            chat_history=session.chat_history,
            tools=self.tools,
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
                if isinstance(action, ToolUse):
                    tool = self._find_tool(action.tool_name)
                    if not tool:
                        result = f"Tool {action.tool_name} not found"
                    else:
                        result = await tool.run(action.instruction, session.sandbox.path)
                    tool_msg = Message(role="tool", content=result)
                    session.chat_history.append(tool_msg)
            ctx.chat_history = session.chat_history
            await asyncio.sleep(0)

