import os
import pathlib
from typing import no_type_check

import yaml

import navigaattori.template_loader as template
from navigaattori import ENCODING, log

LIITOS_VOCABULARY = os.getenv('LIITOS_VOCABULARY', '')
LIITOS_VOCABULARY_IS_EXTERNAL = bool(LIITOS_VOCABULARY)
if not LIITOS_VOCABULARY:
    LIITOS_VOCABULARY = 'templates/liitos_vocabulary.yml'

LIITOS_VOCABULARY_PATH = pathlib.Path('liitos-vocabulary.yml')


@no_type_check
def load() -> object:
    """Later alligator."""
    log.info(f'loading liitos vocabulary from ({LIITOS_VOCABULARY}) ...')
    liitos_vocabulary_data = template.load_resource(LIITOS_VOCABULARY, LIITOS_VOCABULARY_IS_EXTERNAL)
    vocabulary = yaml.safe_load(liitos_vocabulary_data)

    log.info(f'dumping liitos vocabulary to ({LIITOS_VOCABULARY_PATH}) ...')
    with open(LIITOS_VOCABULARY_PATH, 'wt', encoding=ENCODING) as handle:
        yaml.dump(vocabulary, handle)

    return vocabulary


@no_type_check
def tokens(vocabulary: object) -> list[str]:
    """Later alligator."""
    return sorted(vocabulary['tokens'].values())
