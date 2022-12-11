import copy
import pathlib
from typing import no_type_check

import yaml

from navigaattori import DEFAULT_STRUCTURE_NAME, ENCODING, HUB_NAME, STRUCTURES_KEY, log


@no_type_check
def explore(doc_root: str | pathlib.Path, options: dict[str, bool]) -> tuple[int, object]:
    """Later alligator."""
    guess = options.get('guess', False)
    root = pathlib.Path(doc_root)
    if not root.is_dir():
        message = f'root ({root}) is no directory'
        log.error(message)
        return 1, message

    structures_path = root / HUB_NAME
    has_structures_path = True
    if not structures_path.is_file() or not structures_path.stat().st_size:
        message = f'structures file ({structures_path}) does not exist or is empty'
        if not guess:
            log.error(message)
            return 1, message
        has_structures_path = False
        log.warning(message)

    structures = {}
    if has_structures_path:
        with open(structures_path, 'rt', encoding=ENCODING) as handle:
            structures = yaml.safe_load(handle)

    if not structures and not guess:
        message = f'structures information read from file ({structures_path}) is empty'
        log.error(message)
        return 1, message

    if structures and not guess and STRUCTURES_KEY not in structures:
        message = f'structures information is missing the ({STRUCTURES_KEY}) key'
        log.error(message)
        return 1, message

    if not structures and guess:
        log.info(f'guessing target types from recursive search for ({DEFAULT_STRUCTURE_NAME}) files ...')
        target_types = {}
        for path in root.rglob('*'):
            if '.git' not in str(path) and str(path).endswith(DEFAULT_STRUCTURE_NAME):
                t_type = path.parent.name
                t_rel_dir = str(path.parent).split(f'{root}', 1)[1].lstrip('/')
                t_file = path.name
                target_types[t_type] = {
                    'dir': t_rel_dir,
                    'file': t_file,
                    'structure': {},
                    'valid': True,
                }
                log.info(f'- guessed target type ({t_type}) from path ({path})')
    else:
        log.info(f'not guessing but reading target types from ({structures_path}) data instead ...')
        spanning_map = structures[STRUCTURES_KEY]
        if not isinstance(spanning_map, dict):
            message = f'the ({STRUCTURES_KEY}) key does not provide a map of target types to structure paths'
            log.error(message)
            return 1, message

        target_types = {
            t: {
                'dir': str(pathlib.Path(sp).parent),
                'file': pathlib.Path(sp).name,
                'structure': {},
                'valid': True,
            }
            for t, sp in spanning_map.items()
        }

    for target_type, spec in target_types.items():
        log.info(f'screening target type ({target_type}) ...')
        spec_path = root / spec['dir'] / spec['file']
        if not spec_path.is_file() or not spec_path.stat().st_size:
            log.error(f'spec_path file ({spec_path}) for target type ({target_type}) does not exist or is empty')
            target_types[target_type]['valid'] = False

    facet_block = {
        'approvals': '',
        'bind': '',
        'changes': '',
        'meta': '',
        'render': True,
        'formats': [],
        'options': {},
    }
    expected_facet_keys = list(facet_block)
    resource_keys = expected_facet_keys[:4]
    for target_type, spec in target_types.items():
        if not spec['valid']:
            log.info(f'skipping invalid target ({target_type})')
            continue
        log.info(f'assessing target type ({target_type}) ...')
        structure = {}
        spec_path = root / spec['dir'] / spec['file']
        try:
            with open(spec_path, 'rt', encoding=ENCODING) as handle:
                structure = yaml.safe_load(handle)
            if not structure:
                log.error(
                    f'structure information for target type ({target_type}) read from file ({spec_path}) is empty'
                )
                target_types[target_type]['valid'] = False
        except Exception as ex:
            log.error(f'reading spec_path file ({spec_path}) for target type ({target_type}) errs with ({ex})')
            target_types[target_type]['valid'] = False
            continue

        if not structure:
            target_types[target_type]['valid'] = False
            continue

        for target, facet_container in structure.items():
            log.info(f'- assessing target ({target}) with target type ({target_type}) ...')
            target_types[target_type]['structure'][target] = {}
            for facet in facet_container:
                for fk, fd in facet.items():
                    target_types[target_type]['structure'][target][fk] = copy.deepcopy(facet_block)
                    for efk in expected_facet_keys:
                        target_types[target_type]['structure'][target][fk][efk] = fd.get(efk)
                    for erfk in resource_keys:
                        erv = target_types[target_type]['structure'][target][fk][erfk]
                        if not erv or not (root / spec['dir'] / erv).is_file():
                            log.error(
                                f'  + invalid ({erfk}) resource ({erv}) for facet ({fk}) of target ({target})'
                                f' with target type ({target_type}) - resource does not exist or is no file'
                            )
                            target_types[target_type]['valid'] = False

    for target_type, spec in target_types.items():
        log.info(f'reporting target type ({target_type}) ...')
        log.info(f'- {target_type=}:')
        for key, aspect in spec.items():
            if not isinstance(aspect, dict) or not aspect:
                log.info(f'  + {key} -> {aspect}')
            else:
                log.info(f'  + {key} =>')
                for this, that in aspect.items():
                    if not isinstance(that, dict) or not that:
                        log.info(f'    * {this} -> {that}')
                    else:
                        log.info(f'    * {this} =>')
                        for k, v in that.items():
                            if not isinstance(v, dict) or not v:
                                log.info(f'      - {k} -> {v}')
                            else:
                                log.info(f'      - {k} =>')
                                for kf, vf in v.items():
                                    log.info(f'        + {kf} -> {vf}')

    log.warning(expected_facet_keys)
    if any(not spec['valid'] for spec in target_types.values()):
        invalid = sorted(target_type for target_type, spec in target_types.items() if not spec['valid'])
        target_sin_plu = 'target type' if len(invalid) == 1 else 'target types'
        be_sin_plu = 'is' if len(invalid) == 1 else 'are'
        message = f'specifications for {target_sin_plu} ({", ".join(invalid)}) {be_sin_plu} invalid'
        log.error(message)
        return 1, message

    if guess and not has_structures_path:
        guessing_path = pathlib.Path('GUESS')
        guessing_path.mkdir(parents=True, exist_ok=True)

        log.info(f'Dumping proposed global expanded file from guessing to ({guessing_path / "tree.yml"}) ...')
        container = {STRUCTURES_KEY: copy.deepcopy(target_types)}
        with open(guessing_path / 'tree.yml', 'wt', encoding=ENCODING) as handle:
            yaml.dump(container, handle)

        log.info(f'Dumping proposed structures file from guessing to ({guessing_path / HUB_NAME}) ...')
        proposal = {STRUCTURES_KEY: {k: f'{v["dir"]}/{v["file"]}' for k, v in target_types.items()}}
        with open(guessing_path / HUB_NAME, 'wt', encoding=ENCODING) as handle:
            yaml.dump(proposal, handle)

    return 0, target_types
