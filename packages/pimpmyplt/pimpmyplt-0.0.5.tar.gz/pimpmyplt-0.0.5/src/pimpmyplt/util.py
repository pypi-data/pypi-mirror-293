from collections import ChainMap
from typing import Any
from typing import Mapping

from pimpmyplt.pimps import Pimper


def _check_input(objs: list[Any]) -> None:
    allowed_types = (Pimper, dict)
    for obj in objs:
        if not isinstance(obj, allowed_types):
            msg = f"Invalid type: {type(obj)}"
            raise TypeError(msg)


def compose(pimps: list[Pimper | dict[str, Any]]) -> Mapping[str, Any]:
    # Validate input types
    _check_input(pimps)

    # Load collections
    loaded = [p.build() if isinstance(p, Pimper) else p for p in pimps]

    # Return the composed pimps. ChainMap will merge the pimps in a defined
    # order.
    return ChainMap(*loaded)
