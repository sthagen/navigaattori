import copy
import pathlib
from typing import no_type_check

import yaml

from navigaattori import ENCODING, log


@no_type_check
class Changes:
    """Represent a list of changes (tuples of author, [date], issue, [revision], and summary) in sequence."""

    def changes_have_content(self) -> None:
        """Ensure we received a folder to bootstrap."""
        if not self.changes_path.is_file() or not self.changes_path.stat().st_size:
            self.state_code = 1
            self.state_message = f'changes ({self.changes_path}) is no file or empty'
            log.error(self.state_message)

    def load_changes(self) -> None:
        """Load the sequence of changes tuples (author, [date], issue, [revision], and summary)."""
        with open(self.changes_path, 'rt', encoding=ENCODING) as handle:
            data = yaml.safe_load(handle)
        if not data:
            self.state_code = 1
            self.state_message = 'empty changes?'
            log.error(f'changes sequence failed to load any entry from ({self.changes_path})')
            return
        peeled = data.get('changes', []) if isinstance(data, dict) else []
        if not peeled or 'changes' not in data:
            self.state_code = 1
            self.state_message = 'no changes or wrong file?'
            log.error(f'changes sequence failed to load anything from ({self.changes_path})')
            return
        for entry in peeled:
            if not isinstance(entry, dict) or 'author' not in entry or 'summary' not in entry:
                self.state_code = 1
                self.state_message = (
                    f'no map or one of the required keys (author, summary) missing in {entry}'
                    f' of changes read from ({self.changes_path})?'
                )
                log.error(f'changes sequence failed to load entry ({entry}) from ({self.changes_path})')
                return

        self.changes_sequence = []
        for entry in peeled:
            change = {
                'author': entry.get('author', 'AUTHOR-MISSING'),
                'date': entry.get('date', ''),
                'issue': entry.get('issue', ''),
                'revision': entry.get('revision', ''),
                'summary': entry.get('summary', 'SUMMARY-MISSING'),
            }
            self.changes_sequence.append(change)
        self.changes_count = len(self.changes_sequence)
        changes_sin_plu = 'change' if self.changes_count == 1 else 'changes'
        log.info(f'changes sequence loaded {self.changes_count} {changes_sin_plu} from ({self.changes_path}):')
        for entry in self.changes_sequence:
            log.info(f'- {entry}')
        log.info(f'changes sequence successfully loaded from ({self.changes_path}):')

    def __init__(self, changes_path: str | pathlib.Path, options: dict[str, bool]):
        self._options = options
        self.debug: bool = self._options.get('debug', False)
        self.guess: bool = self._options.get('guess', False)
        self.quiet: bool = self._options.get('quiet', False)
        self.verbose: bool = self._options.get('verbose', False)
        self.changes_path: pathlib.Path = pathlib.Path(changes_path)
        self.changes_sequence = []
        self.changes_count = len(self.changes_sequence)
        self.state_code = 0
        self.state_message = ''

        self.changes_have_content()

        if not self.state_code:
            self.load_changes()

        if not self.state_code:
            log.info(f'sequence of changes from ({self.changes_path}) is valid')

    def is_valid(self) -> bool:
        """Is the model valid?"""
        return not self.state_code

    def code_details(self) -> tuple[int, str]:
        """Return an ordered pair of state code and message"""
        return self.state_code, self.state_message

    @no_type_check
    def container(self):
        """Return the changes sequence."""
        return copy.deepcopy(self.changes_sequence)
