from typing import Any

from pimpmyplt.pimps.abc import Pimper


class PimpUseTeX(Pimper):
    def build(self) -> dict[str, Any]:
        return {
            "text.usetex": True,
            "font.family": "serif",
            "font.serif": "cm",
        }
