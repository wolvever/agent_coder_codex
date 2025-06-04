from dataclasses import dataclass, field
from typing import List, Optional

from .events import Message, ToolUse, FinishAction
from .input import UserInput
from .sandbox import Sandbox
from .tools import Tool

@dataclass
class PlanningContext:
    session_id: str
    user_input: UserInput
    chat_history: List[Message]
    tools: List[Tool]
    sandbox: Sandbox
    instruction: str
    searched_chunks: Optional[str] = None

@dataclass
class PlannerStep:
    messages: List[Message] = field(default_factory=list)
    actions: List[object] = field(default_factory=list)

class Planner:
    async def plan(self, ctx: PlanningContext) -> PlannerStep:
        raise NotImplementedError

class EchoPlanner(Planner):
    async def plan(self, ctx: PlanningContext) -> PlannerStep:
        content = f"Echo: {ctx.user_input.text}"
        return PlannerStep(messages=[Message(role="assistant", content=content)],
                           actions=[FinishAction(result=content)])


class ToolPlanner(Planner):
    """Planner that requests a tool run then returns its output."""

    async def plan(self, ctx: PlanningContext) -> PlannerStep:
        # Check if a tool message exists in chat history; if so finish with it.
        for msg in reversed(ctx.chat_history):
            if msg.role == "tool":
                return PlannerStep(actions=[FinishAction(result=msg.content)])

        # Otherwise ask to run the echo tool.
        return PlannerStep(actions=[ToolUse(tool_name="echo", instruction=ctx.user_input.text)])
