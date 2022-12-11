import pathlib

import navigaattori.bind as bind

FIXTURES_ROOT = pathlib.Path('test') / 'fixtures'
BASIC_FIXTURE = FIXTURES_ROOT / 'basic'
EMPTY_FIXTURE = FIXTURES_ROOT / 'empty'
NO_KEY_FIXTURE = FIXTURES_ROOT / 'missing-key'
KEY_NO_MAP_FIXTURE = FIXTURES_ROOT / 'key-no-map'
GUESS_FIXTURE = FIXTURES_ROOT / 'guess'


def test_binder_prelim_no_file():
    binder = bind.Binder('no-file', {})
    assert binder.code_details() == (1, 'binder (no-file) is no file or empty')


def test_binder_prelim_empty_file():
    empty_path = GUESS_FIXTURE / 'foo' / 'empty.md'
    binder = bind.Binder(empty_path, {})
    assert binder.code_details() == (1, f'binder ({empty_path}) is no file or empty')


def test_binder_prelim_spaces_only_file():
    binder = bind.Binder(GUESS_FIXTURE / 'foo' / 'spaces_only.md', {})
    assert binder.code_details() == (1, 'empty binder?')


def test_binder_prelim_pointer_to_folder():
    rel_pointer = 'folder'
    binder = bind.Binder(GUESS_FIXTURE / 'foo' / 'bind-pointer-to-folder.txt', {})
    detail = f'resource ({rel_pointer}) is no file (at {GUESS_FIXTURE / "foo" / rel_pointer})'
    assert binder.code_details() == (1, detail)
