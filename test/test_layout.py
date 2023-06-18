import pathlib

import navigaattori.layout as lay

FIXTURES_ROOT = pathlib.Path('test') / 'fixtures'
BASIC_FIXTURE = FIXTURES_ROOT / 'basic'
EMPTY_FIXTURE = FIXTURES_ROOT / 'empty'
NO_KEY_FIXTURE = FIXTURES_ROOT / 'missing-key'
KEY_NO_MAP_FIXTURE = FIXTURES_ROOT / 'key-no-map'
GUESS_FIXTURE = FIXTURES_ROOT / 'guess'


def test_layout_prelim_no_file():
    layout = lay.Layout('no-file', {})
    assert layout.code_details() == (1, 'layout (no-file) is no file or empty')


def test_layout_prelim_empty_file():
    empty_path = GUESS_FIXTURE / 'foo' / 'empty.md'
    layout = lay.Layout(empty_path, {})
    assert layout.code_details() == (1, f'layout ({empty_path}) is no file or empty')


def test_layout_prelim_spaces_only_file():
    layout = lay.Layout(GUESS_FIXTURE / 'foo' / 'spaces_only.md', {})
    assert layout.code_details() == (1, 'empty layout?')


def test_layout_prelim_pointer_to_folder():
    layout = lay.Layout(GUESS_FIXTURE / 'foo' / 'bind-pointer-to-folder.txt', {})
    assert layout.code_details() == (1, 'missing expected top level key document - no layout or wrong file?')


def test_layout_wrong_key():
    wrong_keys_path = GUESS_FIXTURE / 'foo' / 'meta-default-wrong-top-level-key.yml'
    layout = lay.Layout(wrong_keys_path, {})
    assert layout.code_details() == (1, 'missing expected top level key document - no layout or wrong file?')


def test_meta():
    layout = lay.Layout(GUESS_FIXTURE / 'foo' / 'layout.yml', {})
    assert layout.code_details() == (0, '')
    expected = {
        'layout': {
            'global': {
                'has_approvals': True,
                'has_changes': True,
                'has_notices': True,
            },
        },
    }
    assert layout.container() == expected
    assert layout.is_valid() is True
