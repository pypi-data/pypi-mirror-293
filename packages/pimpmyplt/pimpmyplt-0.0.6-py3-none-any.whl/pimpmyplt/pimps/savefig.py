from dataclasses import dataclass
from pathlib import Path
from typing import Any

from pimpmyplt.pimps.abc import Pimper


@dataclass(kw_only=True, frozen=True)
class _PimpSaveFig:
    directory: Path | None = None  # Only applies to interactive savefig!

    def _root_dict(self) -> dict[str, Any]:
        if self.directory is not None:
            return {"savefig.directory": self.directory}
        return {}


@dataclass(kw_only=True, frozen=True)
class PimpSaveFigPDF(Pimper, _PimpSaveFig):
    def build(self) -> dict[str, Any]:
        out = self._root_dict()
        out["savefig.format"] = "pdf"
        return out


@dataclass(kw_only=True, frozen=True)
class PimpSaveFigPNG(Pimper, _PimpSaveFig):
    dpi: int | None = None

    def build(self) -> dict[str, Any]:
        out = self._root_dict()
        out["savefig.format"] = "png"
        if self.dpi is not None:
            out["savefig.dpi"] = self.dpi
        return out
