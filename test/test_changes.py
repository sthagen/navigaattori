import pathlib

import navigaattori.changes as change

FIXTURES_ROOT = pathlib.Path('test') / 'fixtures'
BASIC_FIXTURE = FIXTURES_ROOT / 'basic'
EMPTY_FIXTURE = FIXTURES_ROOT / 'empty'
NO_KEY_FIXTURE = FIXTURES_ROOT / 'missing-key'
KEY_NO_MAP_FIXTURE = FIXTURES_ROOT / 'key-no-map'
GUESS_FIXTURE = FIXTURES_ROOT / 'guess'


def test_changes_prelim_no_file():
    changes = change.Changes('no-file', {})
    assert changes.code_details() == (1, 'changes (no-file) is no file or empty')


def test_changes_prelim_empty_file():
    empty_path = GUESS_FIXTURE / 'foo' / 'empty.md'
    changes = change.Changes(empty_path, {})
    assert changes.code_details() == (1, f'changes ({empty_path}) is no file or empty')


def test_changes_prelim_spaces_only_file():
    changes = change.Changes(GUESS_FIXTURE / 'foo' / 'spaces_only.md', {})
    assert changes.code_details() == (1, 'empty changes?')


def test_changes_prelim_pointer_to_folder():
    changes = change.Changes(GUESS_FIXTURE / 'foo' / 'bind-pointer-to-folder.txt', {})
    assert changes.code_details() == (1, 'no changes or wrong file?')


def test_changes_wrong_key():
    wrong_keys_path = GUESS_FIXTURE / 'foo' / 'changes-wrong-key.yml'
    changes = change.Changes(wrong_keys_path, {})
    detail = (
        "no map or one of the required keys (author, summary) missing in"
        " {'auhtor': 'An Author', 'date': 'PUBLICATIONDATE', 'issue': '01', 'summary': 'Initial Issue'}"
        f" of changes read from ({wrong_keys_path})?"
    )
    assert changes.code_details() == (1, detail)


def test_changes():
    changes = change.Changes(GUESS_FIXTURE / 'foo' / 'changes.yml', {})
    assert changes.code_details() == (0, '')
    expected = [
        {'author': 'An Author', 'date': 'PUBLICATIONDATE', 'issue': '01', 'revision': '00', 'summary': 'Initial Issue'},
        {'author': 'An Author', 'date': '', 'issue': '01', 'revision': '01', 'summary': 'Fixed a nit'},
    ]
    assert changes.container() == expected
    assert changes.is_valid() is True
