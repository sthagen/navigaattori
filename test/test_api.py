import pathlib

import navigaattori.api as api

FIXTURES_ROOT = pathlib.Path('test') / 'fixtures'
BASIC_FIXTURE = FIXTURES_ROOT / 'basic'
EMPTY_FIXTURE = FIXTURES_ROOT / 'empty'
NO_KEY_FIXTURE = FIXTURES_ROOT / 'missing-key'
KEY_NO_MAP_FIXTURE = FIXTURES_ROOT / 'key-no-map'
GUESS_FIXTURE = FIXTURES_ROOT / 'guess'


def test_explore():
    code, stuff = api.explore(BASIC_FIXTURE, {})
    assert code == 1
    assert stuff


def test_explore_no_dir():
    code, stuff = api.explore(BASIC_FIXTURE / api.HUB_NAME, {})
    assert code == 1
    assert stuff


def test_explore_wrong_dir():
    code, stuff = api.explore(BASIC_FIXTURE / 'foo', {})
    assert code == 1
    assert stuff


def test_explore_structures_empty():
    code, stuff = api.explore(EMPTY_FIXTURE, {})
    assert code == 1
    assert stuff


def test_explore_structures_missing_key():
    code, stuff = api.explore(NO_KEY_FIXTURE, {})
    assert code == 1
    assert stuff


def test_explore_structures_key_no_map():
    code, stuff = api.explore(KEY_NO_MAP_FIXTURE, {})
    assert code == 1
    assert stuff


def test_explore_structures_guess():
    code, stuff = api.explore(GUESS_FIXTURE, options={'guess': True})
    assert code == 0
    assert stuff


def test_binder_prelim_no_file():
    binder = api.Binder('no-file', {})
    assert binder.code_details() == (1, 'binder (no-file) is no file or empty')


def test_binder_prelim_empty_file():
    empty_path = GUESS_FIXTURE / 'foo' / 'empty.md'
    binder = api.Binder(empty_path, {})
    assert binder.code_details() == (1, f'binder ({empty_path}) is no file or empty')


def test_binder_prelim_spaces_only_file():
    binder = api.Binder(GUESS_FIXTURE / 'foo' / 'spaces_only.md', {})
    assert binder.code_details() == (1, 'empty binder?')


def test_binder_prelim_pointer_to_folder():
    rel_pointer = 'folder'
    binder = api.Binder(GUESS_FIXTURE / 'foo' / 'bind-pointer-to-folder.txt', {})
    detail = f'resource ({rel_pointer}) is no file (at {GUESS_FIXTURE / "foo" / rel_pointer})'
    assert binder.code_details() == (1, detail)
