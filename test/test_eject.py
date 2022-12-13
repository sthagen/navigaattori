import yaml

import navigaattori.eject as eject


def test_this_ok(capsys):
    assert eject.this('liitos-vocab') == 0
    out, err = capsys.readouterr()
    assert not err
    assert 'tokens' in out
    interpret_as_yaml = yaml.safe_load(out)
    assert interpret_as_yaml['tokens']['%%_PATCH_%_MAIN_%_TITLE_%%'] == 'title'


def test_this_no_thing(caplog):
    assert eject.this('') == 2
    assert 'eject of template with no name requested' in caplog.text


def test_this_wrong_thing(caplog):
    assert eject.this('unknown-thing') == 2
    assert 'unknown-thing' in caplog.text


def test_this_write_weird_thing(caplog):
    assert eject.this('li', out='/dev/null') == 0
    assert 'requested writing (templates/liitos_vocabulary.yml) to file (null)' in caplog.text


def test_this_write_out_thing(caplog):
    assert eject.this('liitos-vocabulary', out='/tmp/liitos_vocabulary.yml') == 0
