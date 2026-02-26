from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
from typing import Optional, Dict, Any

class RuleType(str, Enum):
    TRIM = "TRIM"
    UPPERCASE = "UPPERCASE"
    REPLACE = "REPLACE"

@dataclass(frozen=True)
class Rule:
    rule_type: RuleType
    column: str
    params: Optional[Dict[str, Any]] = None

    def label(self) -> str:
        if self.rule_type == RuleType.REPLACE:
            old = (self.params or {}).get("old", "")
            new = (self.params or {}).get("new", "")
            return f"{self.rule_type} | {self.column} | '{old}'→'{new}'"
        return f"{self.rule_type} | {self.column}"
