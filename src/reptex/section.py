from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict


@dataclass
class Section:
    template: Path
    context: Dict[str, Any]
