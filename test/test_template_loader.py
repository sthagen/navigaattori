import tempfile

import navigaattori.template_loader as template

STARTSWITH = """\
---
slot_marker: VALUE.SLOT
targets:
  title:
    eol_marker: '%%_PATCH_%_MAIN_%_TITLE_%%'
    default: null
    scope: metadata.tex.in
"""

ENDSWITH = """\
  '%%_PATCH_%_FIXED_%_FONT_%_PACKAGE_%%': fixed_font_package
  '%%_PATCH_%_CODE_%_FONTSIZE_%%': code_fontsize
  '%%_PATCH_%_CHOSEN_%_LOGO_%%': chosen_logo
"""


def test_load_vocab_patch():
    text = template.load_resource('templates/liitos_vocabulary.yml', False)
    assert text.startswith(STARTSWITH)
    assert text.endswith(ENDSWITH)


def test_eject():
    with tempfile.TemporaryDirectory() as tmpdirname:
        assert template.eject([tmpdirname]) == 0
