import copy
import pathlib
from typing import no_type_check

import yaml

from navigaattori import DEFAULT_STRUCTURE_NAME, ENCODING, HUB_NAME, STRUCTURES_KEY, log
from navigaattori.approvals import Approvals
from navigaattori.bind import Binder
from navigaattori.changes import Changes


@no_type_check
class Structures:
    """Model for structures as top level information to navigate all target types."""

    def fs_root_is_dir(self) -> None:
        """Ensure we received a folder to bootstrap."""
        if not self.fs_root.is_dir():
            self.state_code = 1
            self.state_message = f'root ({self.fs_root}) is no directory'
            log.error(self.state_message)

    def explore_structure_path(self) -> None:
        """Try to read from the structures filesystem path."""
        if not self.structures_path.is_file() or not self.structures_path.stat().st_size:
            self.state_message = f'structures file ({self.structures_path}) does not exist or is empty'
            if not self.guess:
                log.error(self.state_message)
                log.info(
                    '... you may want to try the --guess option to the explore command to bootstrap a structures file'
                )
                self.state_code = 1
                return
            self.has_structures_path = False
            log.warning(self.state_message)

    def bootstrap_target_types(self) -> None:
        """Fill in structures and target_types data as per mode (guess or not)."""
        structures = {}
        if self.has_structures_path:
            with open(self.structures_path, 'rt', encoding=ENCODING) as handle:
                structures = yaml.safe_load(handle)

        if not structures and not self.guess:
            self.state_message = f'structures information read from file ({self.structures_path}) is empty'
            log.error(self.state_message)
            self.state_code = 1
            return

        if structures and not self.guess and STRUCTURES_KEY not in structures:
            self.state_message = f'structures information is missing the ({STRUCTURES_KEY}) key'
            log.error(self.state_message)
            self.state_code = 1
            return

        if not structures and self.guess:
            log.info(f'guessing target types from recursive search for ({DEFAULT_STRUCTURE_NAME}) files ...')
            self.target_types = {}
            for path in self.fs_root.rglob('*'):
                if '.git' not in str(path) and str(path).endswith(DEFAULT_STRUCTURE_NAME):
                    t_type = path.parent.name
                    t_rel_dir = str(path.parent).split(f'{self.fs_root}', 1)[1].lstrip('/')
                    t_file = path.name
                    self.target_types[t_type] = {
                        'dir': t_rel_dir,
                        'file': t_file,
                        'structure': {},
                        'valid': True,
                    }
                    log.info(f'- guessed target type ({t_type}) from path ({path})')
        else:
            log.info(f'not guessing but reading target types from ({self.structures_path}) data instead ...')
            spanning_map = structures.get(STRUCTURES_KEY, {})
            if not isinstance(spanning_map, dict) or not spanning_map:
                self.state_message = (
                    f'the ({STRUCTURES_KEY}) key does not provide a map of target types to structure paths'
                )
                log.error(self.state_message)
                self.state_code = 1
                return

            self.target_types = {
                t: {
                    'dir': str(pathlib.Path(sp).parent),
                    'file': pathlib.Path(sp).name,
                    'structure': {},
                    'valid': True,
                }
                for t, sp in spanning_map.items()
            }

    @no_type_check
    def screen_target_types(self) -> None:
        """Ensure we have backing in the file system for all target types."""
        for target_type, spec in self.target_types.items():
            log.info(f'screening target type ({target_type}) ...')
            spec_path = self.fs_root / spec['dir'] / spec['file']
            if not spec_path.is_file() or not spec_path.stat().st_size:
                log.error(f'spec_path file ({spec_path}) for target type ({target_type}) does not exist or is empty')
                self.target_types[target_type]['valid'] = False

    @no_type_check
    def assess_target_types(self) -> None:
        """Assess and eventually fill in information from target types."""
        for target_type, spec in self.target_types.items():
            if not spec['valid']:
                log.info(f'skipping invalid target ({target_type})')
                continue
            log.info(f'assessing target type ({target_type}) ...')
            structure = {}
            spec_path = self.fs_root / spec['dir'] / spec['file']
            try:
                with open(spec_path, 'rt', encoding=ENCODING) as handle:
                    structure = yaml.safe_load(handle)
                if not structure:
                    log.error(
                        f'structure information for target type ({target_type}) read from file ({spec_path}) is empty'
                    )
                    self.target_types[target_type]['valid'] = False
            except Exception as ex:
                log.error(f'reading spec_path file ({spec_path}) for target type ({target_type}) errs with ({ex})')
                self.target_types[target_type]['valid'] = False
                continue

            if not structure:
                self.target_types[target_type]['valid'] = False
                continue

            for target, facet_container in structure.items():
                log.info(f'- assessing target ({target}) with target type ({target_type}) ...')
                self.target_types[target_type]['structure'][target] = {}
                for facet in facet_container:
                    for fk, fd in facet.items():
                        self.target_types[target_type]['structure'][target][fk] = copy.deepcopy(self.facet_block)
                        for efk in self.expected_facet_keys:
                            self.target_types[target_type]['structure'][target][fk][efk] = fd.get(efk)
                        for erfk in self.resource_keys:
                            erv = self.target_types[target_type]['structure'][target][fk][erfk]
                            if not erv or not (self.fs_root / spec['dir'] / erv).is_file():
                                log.error(
                                    f'  + invalid ({erfk}) resource ({erv}) for facet ({fk}) of target ({target})'
                                    f' with target type ({target_type}) - resource does not exist or is no file'
                                )
                                self.target_types[target_type]['valid'] = False
                            else:
                                if erfk == 'approvals':
                                    approvals_path = self.fs_root / self.target_types[target_type]['dir'] / erv
                                    log.info(f'assessing approvals ({approvals_path}) yielding:')
                                    code, details = self.assess_approvals(approvals_path)
                                    if code:
                                        self.target_types[target_type]['valid'] = False
                                elif erfk == 'bind':
                                    binder_path = self.fs_root / self.target_types[target_type]['dir'] / erv
                                    log.info(f'assessing binder ({binder_path}) yielding:')
                                    code, details = self.assess_binder(binder_path)
                                    if code:
                                        self.target_types[target_type]['valid'] = False
                                elif erfk == 'changes':
                                    changes_path = self.fs_root / self.target_types[target_type]['dir'] / erv
                                    log.info(f'assessing changes ({changes_path}) yielding:')
                                    code, details = self.assess_changes(changes_path)
                                    if code:
                                        self.target_types[target_type]['valid'] = False

    @no_type_check
    def assess_approvals(self, approvals_path: str | pathlib.Path):
        """Delegate the verification to an instance of the Approvals class."""
        approvals = Approvals(approvals_path, options=self._options)
        if approvals.is_valid():
            return 0, approvals.container()

        return approvals.code_details()

    @no_type_check
    def assess_binder(self, binder_path: str | pathlib.Path):
        """Delegate the verification to an instance of the Binder class."""
        binder = Binder(binder_path, options=self._options)
        if binder.is_valid():
            return 0, binder.container()

        return binder.code_details()

    @no_type_check
    def assess_changes(self, changes_path: str | pathlib.Path):
        """Delegate the verification to an instance of the Changes class."""
        changes = Changes(changes_path, options=self._options)
        if changes.is_valid():
            return 0, changes.container()

        return changes.code_details()

    def log_assessed_tree(self) -> None:
        """Log out the tree we found."""
        for target_type, spec in self.target_types.items():
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

    def validate_on_screening_level(self) -> None:
        """Let's wrap this up if any invalid target type is present."""
        if not self.target_types:
            self.state_message = f'target types are not present - invalid structures file?'
            log.error(self.state_message)
            self.state_code = 1
            return

        if any(not spec['valid'] for spec in self.target_types.values()):
            invalid = sorted(target_type for target_type, spec in self.target_types.items() if not spec['valid'])
            target_sin_plu = 'target type' if len(invalid) == 1 else 'target types'
            be_sin_plu = 'is' if len(invalid) == 1 else 'are'
            self.state_message = f'specifications for {target_sin_plu} ({", ".join(invalid)}) {be_sin_plu} invalid'
            log.error(self.state_message)
            self.state_code = 1
            return
        self.state_message = 'structures appear to be valid (on file system screening level)'
        log.info(self.state_message)

    @no_type_check
    def dump_guesses(self) -> None:
        """In case we are in guess mode and there is no existing structures file - dump what we suggest."""
        if self.guess and not self.has_structures_path:
            guessing_path = pathlib.Path('GUESS')
            guessing_path.mkdir(parents=True, exist_ok=True)

            log.info(f'dumping proposed global expanded file from guessing to ({guessing_path / "tree.yml"}) ...')
            with open(guessing_path / 'tree.yml', 'wt', encoding=ENCODING) as handle:
                yaml.dump(self.container(complete=True), handle)

            log.info(f'dumping proposed structures file from guessing to ({guessing_path / HUB_NAME}) ...')
            with open(guessing_path / HUB_NAME, 'wt', encoding=ENCODING) as handle:
                yaml.dump(self.structures_map(), handle)

    @no_type_check
    def __init__(self, doc_root: str | pathlib.Path, options: dict[str, bool]):
        self._options = options
        self.debug: bool = self._options.get('debug', False)
        self.guess: bool = self._options.get('guess', False)
        self.quiet: bool = self._options.get('quiet', False)
        self.verbose: bool = self._options.get('verbose', False)
        self.fs_root: pathlib.Path = pathlib.Path(doc_root)
        self.structures_path: pathlib.Path = self.fs_root / HUB_NAME
        self.has_structures_path = True
        self.structures = {}
        self.target_types = {}

        self.facet_block = {
            'approvals': '',  # resource pointer to fs
            'bind': '',  # resource pointer to fs
            'changes': '',  # resource pointer to fs
            'meta': '',  # resource pointer to fs
            'render': True,
            'formats': [],
            'options': {},
        }
        self.expected_facet_keys = list(self.facet_block)
        self.resource_keys = self.expected_facet_keys[:4]

        self.state_code = 0
        self.state_message = ''

        self.fs_root_is_dir()

        if not self.state_code:
            self.explore_structure_path()

        if not self.state_code:
            self.bootstrap_target_types()

        if not self.state_code:
            self.screen_target_types()

        if not self.state_code:
            self.assess_target_types()

        self.log_assessed_tree()
        self.validate_on_screening_level()

        self.dump_guesses()

    def is_valid(self) -> bool:
        """Is the model valid?"""
        return not self.state_code

    def code_details(self) -> tuple[int, str]:
        """Return an ordered pair of state code and message"""
        return self.state_code, self.state_message

    @no_type_check
    def container(self, complete=False):
        """Return either the complete assessed tree or only the target types map."""
        return {STRUCTURES_KEY: copy.deepcopy(self.target_types)} if complete else copy.deepcopy(self.target_types)

    def structures_map(self) -> dict[str, dict[str, str]]:
        """Return the assessed content in the shape of a structures file."""
        return {STRUCTURES_KEY: {k: f'{v["dir"]}/{v["file"]}' for k, v in self.target_types.items()}}
