import copy
import pathlib
from typing import Union, no_type_check

import yaml

from navigaattori import ENCODING, log


@no_type_check
class Layout:
    """Represent the layout."""

    def layout_has_content(self) -> None:
        """Ensure we received a none empty top level layout file to bootstrap from."""
        if not self.layout_path.is_file() or not self.layout_path.stat().st_size:
            self.state_code = 1
            self.state_message = f'layout ({self.layout_path}) is no file or empty'
            log.error(self.state_message)

    def log_assessed_layout(self) -> None:
        """Log out the layout we found."""
        log.info(f'reporting current layout starting from ({self.layout_path}) ...')
        for key, aspect in self.layout.items():
            if not isinstance(aspect, dict) or not aspect:
                log.info(f'- {key} -> {aspect}')
            else:
                log.info(f'- {key} =>')
                for this, that in aspect.items():
                    if not isinstance(that, dict) or not that:
                        log.info(f'  + {this} -> {that}')
                    else:
                        log.info(f'  + {this} =>')
                        for k, v in that.items():
                            if not isinstance(v, dict) or not v:
                                log.info(f'    * {k} -> {v}')
                            else:
                                log.info(f'    * {k} =>')
                                for kf, vf in v.items():
                                    log.info(f'      - {kf} -> {vf}')

    def load_layout(self) -> None:
        """Load the layout data."""
        with open(self.layout_path, 'rt', encoding=ENCODING) as handle:
            data = yaml.safe_load(handle)
        if not data:
            self.state_code = 1
            self.state_message = 'empty layout?'
            log.error(f'layout failed to load any entry from ({self.layout_path})')
            return
        peeled = data.get('layout', []) if isinstance(data, dict) else []
        if not peeled or 'layout' not in data:
            self.state_code = 1
            self.state_message = 'missing expected top level key document - no layout or wrong file?'
            log.error(f'layout failed to load anything from ({self.layout_path})')
            return
        self.layout: dict[str, dict[str, dict[str, bool]]] = copy.deepcopy(data)  # TODO(sthagen) belt and braces
        log.info(f'layout successfully loaded from ({self.layout_path}):')
        self.log_assessed_layout()

    def verify_token_use(self) -> None:
        """Verify layout uses only tokens from the liitos vocabulary."""
        log.info(f'verifying layout starting from ({self.layout_path}) uses only tokens from the liitos vocabulary ...')
        bad_tokens = []
        common_tokens = sorted(self.layout['layout']['global'])
        for token in common_tokens:
            if token not in self.tokens:
                bad_tokens.append(token)
                log.error(f'- unknown token ({token}) in layout')

        if bad_tokens:
            badness = len(bad_tokens)
            tok_sin_plu = 'token' if badness == 1 else 'tokens'
            self.state_code = 1
            self.state_message = (
                f'found {badness} invalid {tok_sin_plu} {tuple(sorted(bad_tokens))}'
                f' in layout loaded completely starting from ({self.layout_path})'
            )
            return

        common_tokens_count = len(common_tokens)
        tok_sin_plu = 'token' if common_tokens_count == 1 else 'tokens'
        token_use = round(100.0 * common_tokens_count / len(self.tokens), 2)
        log.info(f'layout successfully verified {common_tokens_count} {tok_sin_plu} ({token_use}% of vocabulary)')

    def __init__(self, layout_path: Union[str, pathlib.Path], options: dict[str, bool]):
        self._options = options
        self.quiet: bool = self._options.get('quiet', False)
        self.strict: bool = self._options.get('strict', False)
        self.verbose: bool = self._options.get('verbose', False)
        self.guess: bool = self._options.get('guess', False)
        self.layout_path: pathlib.Path = pathlib.Path(layout_path)
        # self.layout: dict[str, dict[str, dict[str, bool]]] = {}
        self.state_code = 0
        self.state_message = ''

        self.layout_has_content()

        self.tokens = ('has_approvals', 'has_changes', 'has_notices')  # HACK A DID ACK

        if not self.state_code:
            self.load_layout()

        if not self.state_code:
            self.verify_token_use()

        if not self.state_code:
            log.info(f'layout from ({self.layout_path}) seems to be valid')

    def is_valid(self) -> bool:
        """Is the model valid?"""
        return not self.state_code

    def code_details(self) -> tuple[int, str]:
        """Return an ordered pair of state code and message"""
        return self.state_code, self.state_message

    @no_type_check
    def container(self):
        """Return the layout."""
        return copy.deepcopy(self.layout)
