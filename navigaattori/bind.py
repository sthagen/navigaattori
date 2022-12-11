import copy
import pathlib
from typing import no_type_check

from navigaattori import ENCODING, log


@no_type_check
class Binder:
    """Represent a list of resources to be bound in sequence after resolving all parts."""

    def binder_has_content(self) -> None:
        """Ensure we received a folder to bootstrap."""
        if not self.binder_path.is_file() or not self.binder_path.stat().st_size:
            self.state_code = 1
            self.state_message = f'binder ({self.binder_path}) is no file or empty'
            log.error(self.state_message)

    def load_binder(self) -> None:
        """Load the sequence of resource paths."""
        with open(self.binder_path, 'rt', encoding=ENCODING) as handle:
            self.resource_sequence = [line.strip() for line in handle.readlines() if line.strip()]
        self.resource_count = len(self.resource_sequence)
        res_sin_plu = 'resource' if self.resource_count == 1 else 'resources'
        if not self.resource_count:
            self.state_code = 1
            self.state_message = 'empty binder?'
            log.error(f'binder sequence failed to load any entry from ({self.binder_path})')
        else:
            log.info(f'binder sequence loaded {self.resource_count} {res_sin_plu} from ({self.binder_path}):')
            for resource in self.resource_sequence:
                log.info(f'- {resource}')
            log.info(f'binder sequence successfully loaded from ({self.binder_path}):')

    def assess_resources(self) -> None:
        """Inspect the sequence of resource paths (empty targets are OK)."""
        for resource in self.resource_sequence:
            if not (self.binder_base / resource).is_file():
                self.state_code = 1
                self.state_message = f'resource ({resource}) is no file (at {self.binder_base / resource})'
                log.error(self.state_message)
                continue
            log.info(f'- resource ({resource}) points to file (at {self.binder_base / resource})')

    def __init__(self, binder_path: str | pathlib.Path, options: dict[str, bool]):
        self._options = options
        self.debug: bool = self._options.get('debug', False)
        self.guess: bool = self._options.get('guess', False)
        self.quiet: bool = self._options.get('quiet', False)
        self.verbose: bool = self._options.get('verbose', False)
        self.binder_path: pathlib.Path = pathlib.Path(binder_path)
        self.binder_base = self.binder_path.parent
        self.resource_sequence = []
        self.resource_count = len(self.resource_sequence)
        self.state_code = 0
        self.state_message = ''

        self.binder_has_content()

        if not self.state_code:
            self.load_binder()

        if not self.state_code:
            self.assess_resources()

        if not self.state_code:
            log.info(f'sequence of resources of ({self.binder_path}) is valid')

    def is_valid(self) -> bool:
        """Is the model valid?"""
        return not self.state_code

    def code_details(self) -> tuple[int, str]:
        """Return an ordered pair of state code and message"""
        return self.state_code, self.state_message

    @no_type_check
    def container(self):
        """Return the resource sequence."""
        return copy.deepcopy(self.resource_sequence)
