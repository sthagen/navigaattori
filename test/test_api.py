import pathlib

import navigaattori.api as api
from navigaattori import HUB_NAME

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
    code, stuff = api.explore(BASIC_FIXTURE / HUB_NAME, {})
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
