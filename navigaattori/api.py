import pathlib
from typing import no_type_check

from navigaattori.structures import Structures


@no_type_check
def explore(doc_root: str | pathlib.Path, options: dict[str, bool]) -> tuple[int, object]:
    """Later alligator."""
    structures = Structures(doc_root, options=options)
    if structures.is_valid():
        return 0, structures.container()

    return structures.code_details()
