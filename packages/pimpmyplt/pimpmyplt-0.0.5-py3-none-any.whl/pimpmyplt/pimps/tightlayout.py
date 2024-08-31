from typing import Any

from pimpmyplt.pimps.abc import Pimper


class PimpTightLayout(Pimper):
    def build(self) -> dict[str, Any]:
        # Setting `figure.autolayout` to `True` behaves like `tight_layout`, see
        # https://github.com/matplotlib/matplotlib/blob/a254b687df97cda8c6affa37a1dfcf213f8e6c3a/lib/matplotlib/figure.py#L2636-L2640

        return {"figure.autolayout": True}
