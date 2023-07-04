"""Loader function for templates."""
import pathlib
import pkgutil
from typing import Union

from navigaattori import ENCODING, log

RESOURCES = ('templates/liitos_vocabulary.yml',)


def load_resource(resource: str, is_complete_path: bool = False) -> str:
    """Load the template either from the package resources or an external path."""
    if is_complete_path:
        log.debug(f'loading resource from external source ({resource})')
        with open(resource, 'rt', encoding=ENCODING) as handle:
            return handle.read()
    else:
        return pkgutil.get_data(__package__, resource).decode(encoding=ENCODING)  # type: ignore


def eject(argv: Union[list[str], None] = None) -> int:
    """Eject the templates into the folder given (default EJECTED) and create the folder if it does not exist."""
    argv = argv if argv else ['']
    into = argv[0]
    if not into.strip():
        into = 'EJECTED'
    into_path = pathlib.Path(into)
    (into_path / 'templates').mkdir(parents=True, exist_ok=True)
    for resource in RESOURCES:
        write_to = into_path / resource
        log.debug(f'- ejecting resource ({resource}) to ({write_to})')
        data = pkgutil.get_data(__package__, resource).decode(encoding=ENCODING)  # type: ignore
        with open(write_to, 'wt', encoding=ENCODING) as target:
            target.write(data)

    return 0
