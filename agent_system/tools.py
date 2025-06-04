import asyncio
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

@dataclass
class Tool:
    name: str
    description: str

    async def run(self, instruction: str, sandbox: Path) -> str:
        raise NotImplementedError

class GitTool(Tool):
    def __init__(self):
        super().__init__(name="git", description="Interact with git repositories")

    async def run(self, instruction: str, sandbox: Path) -> str:
        proc = await asyncio.create_subprocess_shell(instruction, cwd=sandbox,
                                                     stdout=subprocess.PIPE,
                                                     stderr=subprocess.STDOUT)
        out, _ = await proc.communicate()
        return out.decode()

class TestTool(Tool):
    def __init__(self):
        super().__init__(name="pytest", description="Run pytest in sandbox")

    async def run(self, instruction: str, sandbox: Path) -> str:
        cmd = f"pytest {instruction}"
        proc = await asyncio.create_subprocess_shell(cmd, cwd=sandbox,
                                                     stdout=subprocess.PIPE,
                                                     stderr=subprocess.STDOUT)
        out, _ = await proc.communicate()
        return out.decode()


class EchoTool(Tool):
    """Simple tool that echoes the instruction."""

    def __init__(self):
        super().__init__(name="echo", description="Echo instruction")

    async def run(self, instruction: str, sandbox: Path) -> str:
        return instruction
