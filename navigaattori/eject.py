"""Eject templates and configurations."""
import pathlib

import navigaattori.template_loader as template
from navigaattori import ENCODING, log

THINGS = {
    'liitos-vocabulary-yaml': (LIIIOS_VOCABULARY_YAML := 'templates/liitos_vocabulary.yml'),
}


def this(thing: str, out: str = '') -> int:
    """Later Alligator."""
    if not thing:
        log.error('eject of template with no name requested')
        log.info(f'templates known: ({", ".join(sorted(THINGS))})')
        return 2
    guesses = sorted(entry for entry in THINGS if entry.startswith(thing))
    if not guesses:
        log.error(f'eject of unknown template ({thing}) requested')
        log.info(f'templates known: ({", ".join(sorted(THINGS))})')
        return 2
    if len(guesses) > 1:
        log.error(f'eject of ambiguous template ({thing}) requested - matches ({", ".join(guesses)})')
        return 2
    content = template.load_resource(THINGS[guesses[0]], False)
    if not out:
        print(content)
        return 0

    out_path = pathlib.Path(out)
    out_name = out_path.name
    if not THINGS[guesses[0]].endswith(out_name):
        log.warning(f'requested writing ({THINGS[guesses[0]]}) to file ({out_name})')
    with open(out_path, 'wt', encoding=ENCODING) as handle:
        handle.write(content)
    return 0
