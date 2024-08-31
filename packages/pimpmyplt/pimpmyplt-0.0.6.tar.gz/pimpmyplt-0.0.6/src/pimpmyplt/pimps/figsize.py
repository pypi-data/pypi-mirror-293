import re
from dataclasses import dataclass
from typing import Any
from typing import Literal

from pimpmyplt.pimps.abc import Pimper


@dataclass(kw_only=True, frozen=True)
class PimpFigSizeDIN(Pimper):
    din_format: str  # Like A1, A4, etc.
    mode: Literal["landscape", "portrait"]

    def _validated_din_number(self) -> int:
        validated = re.fullmatch(r"[a|A](\d+)", self.din_format)
        if validated is None:
            msg = f"Unknown DIN format '{self.din_format}'"
            raise ValueError(msg)
        return int(validated[1])

    def __post_init__(self) -> None:
        _ = self._validated_din_number()

    def build(self) -> dict[str, Any]:
        n = self._validated_din_number()
        dim0 = 46.82 * 0.5 ** (0.5 * n)
        dim1 = 33.11 * 0.5 ** (0.5 * n)
        if self.mode == "landscape":
            return {"figure.figsize": (dim0, dim1)}
        return {"figure.figsize": (dim1, dim0)}


@dataclass(kw_only=True, frozen=True)
class PimpFigSizeCustom(Pimper):
    width: float
    height: float

    def build(self) -> dict[str, Any]:
        return {"figure.figsize": (self.width, self.height)}
