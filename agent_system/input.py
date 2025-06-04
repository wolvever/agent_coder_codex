from dataclasses import dataclass, field
from pathlib import Path
from typing import List

@dataclass
class UserInput:
    """Multi-modal user input."""

    text: str
    files: List[Path] = field(default_factory=list)
    images: List[Path] = field(default_factory=list)
