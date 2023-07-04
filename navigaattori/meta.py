import copy
import pathlib
from typing import Union, no_type_check

import yaml

import navigaattori.liitos_meta as voc
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

    def log_assessed_meta(self) -> None:
        """Log out the meta we found."""
        log.info(f'reporting current metadata starting from ({self.meta_top_path}) ...')
        for key, aspect in self.metadata.items():
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
        self.log_assessed_meta()

    def load_meta_import(self) -> None:
        """Import any metadata if document/import found and valid."""
        if 'import' in self.metadata['document']:
            base_meta_path = self.meta_top_base / self.metadata['document']['import']
            log.info(f'- trying to import metadata from ({base_meta_path})')
            if not base_meta_path.is_file() or not base_meta_path.stat().st_size:
                self.state_code = 1
                self.state_message = 'missing expected top level key document - no metadata or wrong file?'
                log.error(
                    f'metadata declares import of base data from ({base_meta_path.name})'
                    f' but failed to find non-empty base file at {base_meta_path}'
                )
                return
            with open(base_meta_path, 'rt', encoding=ENCODING) as handle:
                base_data = yaml.safe_load(handle)
            for key, value in self.metadata['document']['patch'].items():
                base_data['document']['common'][key] = value
            self.metadata = base_data
        log.info(f'metadata successfully loaded completely starting from ({self.meta_top_path}):')
        self.log_assessed_meta()

    def verify_token_use(self) -> None:
        """Verify metadata uses only tokens from the liitos vocabulary."""
        log.info(
            f'verifying metadata starting from ({self.meta_top_path}) uses only tokens from the liitos vocabulary ...'
        )
        bad_tokens = []
        common_tokens = sorted(self.metadata['document']['common'])
        for token in common_tokens:
            if token not in self.tokens:
                bad_tokens.append(token)
                log.error(f'- unknown token ({token}) in metadata')

        if bad_tokens:
            badness = len(bad_tokens)
            tok_sin_plu = 'token' if badness == 1 else 'tokens'
            self.state_code = 1
            self.state_message = (
                f'found {badness} invalid {tok_sin_plu} {tuple(sorted(bad_tokens))}'
                f' in metadata loaded completely starting from ({self.meta_top_path})'
            )
            return

        common_tokens_count = len(common_tokens)
        tok_sin_plu = 'token' if common_tokens_count == 1 else 'tokens'
        token_use = round(100.0 * common_tokens_count / len(self.tokens), 2)
        log.info(f'metadata successfully verified {common_tokens_count} {tok_sin_plu} ({token_use}% of vocabulary)')

    def __init__(self, meta_top_path: Union[str, pathlib.Path], options: dict[str, bool]):
        self._options = options
        self.quiet: bool = self._options.get('quiet', False)
        self.strict: bool = self._options.get('strict', False)
        self.verbose: bool = self._options.get('verbose', False)
        self.guess: bool = self._options.get('guess', False)
        self.meta_top_path: pathlib.Path = pathlib.Path(meta_top_path)
        self.meta_top_base = self.meta_top_path.parent
        self.metadata = {}
        self.state_code = 0
        self.state_message = ''

        self.meta_top_has_content()

        self.vocabulary = voc.load()
        self.tokens = voc.tokens(self.vocabulary)

        if not self.state_code:
            self.load_meta_top()

        if not self.state_code:
            self.load_meta_import()

        if not self.state_code:
            self.verify_token_use()

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
