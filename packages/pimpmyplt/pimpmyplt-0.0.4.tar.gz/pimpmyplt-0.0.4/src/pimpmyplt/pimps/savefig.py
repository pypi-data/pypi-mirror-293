from dataclasses import dataclass
from typing import Any
from typing import Literal

from pimpmyplt.pimps.abc import Pimper


@dataclass(kw_only=True, frozen=True)
class PimpSaveFig(Pimper):
    dpi: int
    format: Literal["png", "pdf"]

    def build(self) -> dict[str, Any]:
        return {
            "savefig.format": self.format,
            "savefig.dpi": self.dpi,
        }
