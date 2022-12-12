import copy
import pathlib
from typing import no_type_check

import yaml

from navigaattori import ENCODING, log


@no_type_check
class Meta:
    """Represent the metadata (including any imports)."""

    def meta_top_has_content(self) -> None:
        """Ensure we received a none empty top level metadata file to bootstrap from."""
        if not self.meta_top_path.is_file() or not self.meta_top_path.stat().st_size:
            self.state_code = 1
            self.state_message = f'meta ({self.meta_top_path}) is no file or empty'
            log.error(self.state_message)

    def load_meta_top(self) -> None:
        """Load the top level meta data."""
        with open(self.meta_top_path, 'rt', encoding=ENCODING) as handle:
            data = yaml.safe_load(handle)
        if not data:
            self.state_code = 1
            self.state_message = 'empty metadata?'
            log.error(f'meta failed to load any entry from ({self.meta_top_path})')
            return
        peeled = data.get('document', []) if isinstance(data, dict) else []
        if not peeled or 'document' not in data:
            self.state_code = 1
            self.state_message = 'missing expected top level key document - no metadata or wrong file?'
            log.error(f'meta failed to load anything from ({self.meta_top_path})')
            return
        self.metadata = copy.deepcopy(data)  # TODO(sthagen) belt and braces
        log.info(f'top level metadata successfully loaded from ({self.meta_top_path}):')

    def __init__(self, meta_top_path: str | pathlib.Path, options: dict[str, bool]):
        self._options = options
        self.quiet: bool = self._options.get('quiet', False)
        self.strict: bool = self._options.get('strict', False)
        self.verbose: bool = self._options.get('verbose', False)
        self.guess: bool = self._options.get('guess', False)
        self.meta_top_path: pathlib.Path = pathlib.Path(meta_top_path)
        self.metadata = {}
        self.state_code = 0
        self.state_message = ''

        self.meta_top_has_content()

        if not self.state_code:
            self.load_meta_top()

        if not self.state_code:
            log.info(f'metadata from ({self.meta_top_path}) seems to be valid')

    def is_valid(self) -> bool:
        """Is the model valid?"""
        return not self.state_code

    def code_details(self) -> tuple[int, str]:
        """Return an ordered pair of state code and message"""
        return self.state_code, self.state_message

    @no_type_check
    def container(self):
        """Return the metadata."""
        return copy.deepcopy(self.metadata)
