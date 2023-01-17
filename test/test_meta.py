import pathlib

import navigaattori.meta as meta

FIXTURES_ROOT = pathlib.Path('test') / 'fixtures'
BASIC_FIXTURE = FIXTURES_ROOT / 'basic'
EMPTY_FIXTURE = FIXTURES_ROOT / 'empty'
NO_KEY_FIXTURE = FIXTURES_ROOT / 'missing-key'
KEY_NO_MAP_FIXTURE = FIXTURES_ROOT / 'key-no-map'
GUESS_FIXTURE = FIXTURES_ROOT / 'guess'


def test_meta_prelim_no_file():
    metadata = meta.Meta('no-file', {})
    assert metadata.code_details() == (1, 'meta (no-file) is no file or empty')


def test_meta_prelim_empty_file():
    empty_path = GUESS_FIXTURE / 'foo' / 'empty.md'
    metadata = meta.Meta(empty_path, {})
    assert metadata.code_details() == (1, f'meta ({empty_path}) is no file or empty')


def test_meta_prelim_spaces_only_file():
    metadata = meta.Meta(GUESS_FIXTURE / 'foo' / 'spaces_only.md', {})
    assert metadata.code_details() == (1, 'empty metadata?')


def test_meta_prelim_pointer_to_folder():
    metadata = meta.Meta(GUESS_FIXTURE / 'foo' / 'bind-pointer-to-folder.txt', {})
    assert metadata.code_details() == (1, 'missing expected top level key document - no metadata or wrong file?')


def test_meta_wrong_key():
    wrong_keys_path = GUESS_FIXTURE / 'foo' / 'meta-default-wrong-top-level-key.yml'
    metadata = meta.Meta(wrong_keys_path, {})
    assert metadata.code_details() == (1, 'missing expected top level key document - no metadata or wrong file?')


def test_meta():
    metadata = meta.Meta(GUESS_FIXTURE / 'foo' / 'meta-default.yml', {})
    assert metadata.code_details() == (0, '')
    expected = {
        'document': {
            'common': {
                'approvals_adjustable_vertical_space': '2.5em',
                'approvals_date_and_signature_label': 'Date and ' + 'Signature',
                'approvals_name_label': 'Name',
                'approvals_role_label': 'Approvals',
                'bold_font': 'ITCFranklinGothicStd-Demi',
                'bold_italic_font': 'ITCFranklinGothicStd-DemiIt',
                'change_log_author_label': 'Author',
                'change_log_date_label': 'Date',
                'change_log_description_label': 'Description',
                'change_log_issue_label': 'Iss.',
                'change_log_revision_label': 'Rev.',
                'chosen_logo': '/opt/logo/liitos-logo.png',
                'code_fontsize': '\\scriptsize',
                'fixed_font_package': 'sourcecodepro',
                'font_path': '/opt/fonts/',
                'font_suffix': '.otf',
                'footer_frame_note': 'VERY CONSEQUENTIAL',
                'footer_page_number_prefix': 'Page',
                'header_date': 'PUBLICATIONDATE',
                'header_id': 'P99999',
                'header_issue_revision_combined': None,
                'header_title': 'Ttt Tt',
                'header_type': 'Engineering Document',
                'issue': '01',
                'italic_font': 'ITCFranklinGothicStd-BookIt',
                'list_of_figures': '',
                'list_of_tables': '',
                'main_font': 'ITCFranklinGothicStd-Book',
                'proprietary_information': '/opt/legal/proprietary_information.txt',
                'revision': '00',
                'sub_title': 'The Deep Spec',
                'title': 'Ttt Tt Tt',
                'toc_level': 3,
            },
        },
    }
    assert metadata.container() == expected
    assert metadata.is_valid() is True
