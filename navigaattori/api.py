import pathlib

import yaml

from navigaattori import DEFAULT_HUB_NAME, DEFAULT_STRUCTURE_NAME, ENCODING, log


def explore(doc_root: str | pathlib.Path, options: dict[str, bool]) -> tuple[int, object]:
    """Later alligator."""
    root = pathlib.Path(doc_root)
    if not root.is_dir():
        message = f'root ({root}) is no directory'
        log.error(message)
        return 1, message

    structures_path = root / DEFAULT_HUB_NAME
    if not structures_path.is_file() or not structures_path.stat().st_size:
        message = f'structures file ({structures_path}) does not exist or is empty'
        log.error(message)
        return 1, message

    with open(structures_path, 'rt', encoding=ENCODING) as handle:
        structures = yaml.safe_load(handle)

    return 0, structures
