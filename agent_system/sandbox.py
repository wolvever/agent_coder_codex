from dataclasses import dataclass
from pathlib import Path
from typing import List
import subprocess

@dataclass
class Sandbox:
    """Simple sandbox for running commands and manipulating files."""

    path: Path

    def __post_init__(self) -> None:
        self.path.mkdir(parents=True, exist_ok=True)

    def run(self, command: str) -> str:
        """Run a shell command inside the sandbox and return combined output."""
        proc = subprocess.run(
            command,
            cwd=self.path,
            shell=True,
            capture_output=True,
            text=True,
        )
        return proc.stdout + proc.stderr

    def write_file(self, relative_path: str, data: bytes) -> None:
        file_path = self.path / relative_path
        file_path.parent.mkdir(parents=True, exist_ok=True)
        with open(file_path, "wb") as f:
            f.write(data)

    def read_file(self, relative_path: str) -> bytes:
        with open(self.path / relative_path, "rb") as f:
            return f.read()

    def list_files(self) -> List[str]:
        return [str(p.relative_to(self.path)) for p in self.path.rglob("*") if p.is_file()]
