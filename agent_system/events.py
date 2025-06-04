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
