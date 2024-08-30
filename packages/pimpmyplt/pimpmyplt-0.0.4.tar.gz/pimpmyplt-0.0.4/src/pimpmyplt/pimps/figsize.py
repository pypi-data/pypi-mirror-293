from dataclasses import dataclass
from typing import Any
from typing import Literal

from pimpmyplt.pimps.abc import Pimper


@dataclass(kw_only=True, frozen=True)
class PimpFigSizeDINA(Pimper):
    din_number: int
    mode: Literal["landscape", "portrait"]

    def build(self) -> dict[str, Any]:
        dim0 = 46.82 * 0.5 ** (0.5 * self.din_number)
        dim1 = 33.11 * 0.5 ** (0.5 * self.din_number)
        if self.mode == "landscape":
            return {"figure.figsize": (dim0, dim1)}
        return {"figure.figsize": (dim1, dim0)}
