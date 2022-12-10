import pathlib

import navigaattori.api as api

BASIC_FIXTURE = pathlib.Path('test') / 'fixtures' / 'basic'


def test_explore():
    code, stuff = api.explore(BASIC_FIXTURE, {})
    assert code == 1
    assert stuff
