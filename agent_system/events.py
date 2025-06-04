"""Event and action primitives shared between planner and agent."""

from dataclasses import dataclass
from typing import List

@dataclass
class Message:
    role: str
    content: str

@dataclass
class ToolUse:
    tool_name: str
    instruction: str

@dataclass
class FinishAction:
    result: str

@dataclass
class TaskBegin:
    """Event signalling start of a task."""

    description: str


@dataclass
class TaskEnd:
    """Event signalling completion of a task."""

    summary: str
