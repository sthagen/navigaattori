import copy
import pathlib
from typing import no_type_check

import yaml

from navigaattori import ENCODING, log


@no_type_check
class Approvals:
    """Represent a list of approvals (pairs of role and name) in sequence."""

    def approvals_have_content(self) -> None:
        """Ensure we received a folder to bootstrap."""
        if not self.approvals_path.is_file() or not self.approvals_path.stat().st_size:
            self.state_code = 1
            self.state_message = f'approvals ({self.approvals_path}) is no file or empty'
            log.error(self.state_message)

    def load_approvals(self) -> None:
        """Load the sequence of approval pairs (role, name)."""
        with open(self.approvals_path, 'rt', encoding=ENCODING) as handle:
            data = yaml.safe_load(handle)
        if not data:
            self.state_code = 1
            self.state_message = 'empty approvals?'
            log.error(f'approval sequence failed to load any entry from ({self.approvals_path})')
            return
        peeled = data.get('approvals', []) if isinstance(data, dict) else []
        if not peeled or 'approvals' not in data:
            self.state_code = 1
            self.state_message = 'no approvals or wrong file?'
            log.error(f'approval sequence failed to load anything from ({self.approvals_path})')
            return
        for entry in peeled:
            if not isinstance(entry, dict) or 'role' not in entry or 'name' not in entry:
                self.state_code = 1
                self.state_message = (
                    f'no map or one of the keys (role, name) missing in {entry}'
                    f' of approvals read from ({self.approvals_path})?'
                )
                log.error(f'approval sequence failed to load entry ({entry}) from ({self.approvals_path})')
                return

        self.approvals_sequence = [{'role': entry['role'], 'name': entry['name']} for entry in peeled]
        self.approvals_count = len(self.approvals_sequence)
        approval_sin_plu = 'approval' if self.approvals_count == 1 else 'approvals'
        log.info(f'approvals sequence loaded {self.approvals_count} {approval_sin_plu} from ({self.approvals_path}):')
        for entry in self.approvals_sequence:
            log.info(f'- {entry}')
        log.info(f'approvals sequence successfully loaded from ({self.approvals_path}):')

    def __init__(self, approvals_path: str | pathlib.Path, options: dict[str, bool]):
        self._options = options
        self.debug: bool = self._options.get('debug', False)
        self.guess: bool = self._options.get('guess', False)
        self.quiet: bool = self._options.get('quiet', False)
        self.verbose: bool = self._options.get('verbose', False)
        self.approvals_path: pathlib.Path = pathlib.Path(approvals_path)
        self.approvals_sequence = []
        self.approvals_count = len(self.approvals_sequence)
        self.state_code = 0
        self.state_message = ''

        self.approvals_have_content()

        if not self.state_code:
            self.load_approvals()

        if not self.state_code:
            log.info(f'sequence of approvals from ({self.approvals_path}) is valid')

    def is_valid(self) -> bool:
        """Is the model valid?"""
        return not self.state_code

    def code_details(self) -> tuple[int, str]:
        """Return an ordered pair of state code and message"""
        return self.state_code, self.state_message

    @no_type_check
    def container(self):
        """Return the approvals sequence."""
        return copy.deepcopy(self.approvals_sequence)
