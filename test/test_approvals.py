import pathlib

import navigaattori.approvals as approve

FIXTURES_ROOT = pathlib.Path('test') / 'fixtures'
BASIC_FIXTURE = FIXTURES_ROOT / 'basic'
EMPTY_FIXTURE = FIXTURES_ROOT / 'empty'
NO_KEY_FIXTURE = FIXTURES_ROOT / 'missing-key'
KEY_NO_MAP_FIXTURE = FIXTURES_ROOT / 'key-no-map'
GUESS_FIXTURE = FIXTURES_ROOT / 'guess'


def test_approvals_prelim_no_file():
    approvals = approve.Approvals('no-file', {})
    assert approvals.code_details() == (1, 'approvals (no-file) is no file or empty')


def test_approvals_prelim_empty_file():
    empty_path = GUESS_FIXTURE / 'foo' / 'empty.md'
    approvals = approve.Approvals(empty_path, {})
    assert approvals.code_details() == (1, f'approvals ({empty_path}) is no file or empty')


def test_approvals_prelim_spaces_only_file():
    approvals = approve.Approvals(GUESS_FIXTURE / 'foo' / 'spaces_only.md', {})
    assert approvals.code_details() == (1, 'empty approvals?')


def test_approvals_prelim_pointer_to_folder():
    approvals = approve.Approvals(GUESS_FIXTURE / 'foo' / 'bind-pointer-to-folder.txt', {})
    assert approvals.code_details() == (1, 'no approvals or wrong file?')


def test_approvals_wrong_key():
    wrong_keys_path = GUESS_FIXTURE / 'foo' / 'approvals-wrong-key.yml'
    approvals = approve.Approvals(wrong_keys_path, {})
    detail = (
        "no map or one of the keys (role, name) missing in {'name': 'A Reviewer', 'rloe': 'Review'}"
        f" of approvals read from ({wrong_keys_path})?"
    )
    assert approvals.code_details() == (1, detail)


def test_approvals():
    approvals = approve.Approvals(GUESS_FIXTURE / 'foo' / 'approvals.yml', {})
    assert approvals.code_details() == (0, '')
    expected = [
        {'role': 'Author', 'name': 'An Author'},
        {'role': 'Review', 'name': 'A Reviewer'},
        {'role': 'Approved', 'name': 'An App Rover'},
    ]
    assert approvals.container() == expected
    assert approvals.is_valid() is True
