import pathlib

import yaml

from navigaattori import ENCODING, HUB_NAME, STRUCTURES_KEY, log


def explore(doc_root: str | pathlib.Path, options: dict[str, bool]) -> tuple[int, object]:
    """Later alligator."""
    root = pathlib.Path(doc_root)
    if not root.is_dir():
        message = f'root ({root}) is no directory'
        log.error(message)
        return 1, message

    structures_path = root / HUB_NAME
    if not structures_path.is_file() or not structures_path.stat().st_size:
        message = f'structures file ({structures_path}) does not exist or is empty'
        log.error(message)
        return 1, message

    with open(structures_path, 'rt', encoding=ENCODING) as handle:
        structures = yaml.safe_load(handle)

    if not structures:
        message = f'structures information read from file ({structures_path}) is empty'
        log.error(message)
        return 1, message

    if STRUCTURES_KEY not in structures:
        message = f'structures information is missing the ({STRUCTURES_KEY}) key'
        log.error(message)
        return 1, message

    spanning_map = structures[STRUCTURES_KEY]
    if not isinstance(spanning_map, dict):
        message = f'the ({STRUCTURES_KEY}) key does not provide a map of targets to structure paths'
        log.error(message)
        return 1, message

    targets = {
        t: {
            'dir': str(pathlib.Path(sp).parent),
            'file': str(pathlib.Path(sp).name),
            'structure': {
                'approvals': None,
                'bind': None,
                'changes': None,
                'meta': None,
                'render': True,
                'formats': [],
                'options': {},
            },
            'valid': True,
        }
        for t, sp in spanning_map.items()
    }

    for target, spec in targets.items():
        spec_path = root / spec['dir'] / spec['file']  # type: ignore
        if not spec_path.is_file() or not spec_path.stat().st_size:
            log.error(f'spec_path file ({spec_path}) for target ({target}) does not exist or is empty')
            targets[target]['valid'] = False

    for target, spec in targets.items():
        if not spec['valid']:
            log.debug(f'skipping invalid target ({target})')
            continue
        spec_path = root / spec['dir'] / spec['file']  # type: ignore
        try:
            with open(spec_path, 'rt', encoding=ENCODING) as handle:
                structure = yaml.safe_load(handle)
            if not structure:
                log.error(f'structure information for target ({target}) read from file ({spec_path}) is empty')
                targets[target]['valid'] = False
        except Exception as ex:
            log.error(f'reading spec_path file ({spec_path}) for target ({target}) errs with ({ex})')
            targets[target]['valid'] = False

    log.info(targets)
    if any(not spec['valid'] for spec in targets.values()):
        message = f'specifications for targets not all valid'
        log.error(message)
        return 1, message

    return 0, structures
