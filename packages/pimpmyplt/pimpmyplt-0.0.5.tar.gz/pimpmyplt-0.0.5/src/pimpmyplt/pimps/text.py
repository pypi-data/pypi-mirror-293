from dataclasses import dataclass
from typing import Any

from pimpmyplt.pimps.abc import Pimper


@dataclass(kw_only=True, frozen=True)
class PimpText(Pimper):
    size: int = 11

    def build(self) -> dict[str, Any]:
        return {"font.size": self.size}
