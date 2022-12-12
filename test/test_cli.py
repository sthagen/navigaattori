import pathlib

from typer.testing import CliRunner

import navigaattori
from navigaattori.cli import app

runner = CliRunner()

BASIC_FIXTURE = pathlib.Path('test') / 'fixtures' / 'basic'
GUESS_FIXTURE = pathlib.Path('test') / 'fixtures' / 'guess'


def setup():
    pass


def teardown():
    pass


def test_version_ok():
    result = runner.invoke(app, ['version'])
    assert result.exit_code == 0
    assert f'version {navigaattori.__version__}' in result.stdout


def test_explore():
    result = runner.invoke(app, ['explore', str(BASIC_FIXTURE)])
    assert result.exit_code == 1


def test_explore_no_doc_root():
    result = runner.invoke(app, ['explore', '-s'])
    assert result.exit_code == 2


def test_explore_doc_root_not_existing():
    result = runner.invoke(app, ['explore', 'nothing-here'])
    assert result.exit_code == 2


def test_explore_strict():
    result = runner.invoke(app, ['explore', '-g', '-s', str(GUESS_FIXTURE)])
    assert result.exit_code == 0


def test_explore_verbose():
    result = runner.invoke(app, ['explore', '--guess', '-v', str(GUESS_FIXTURE)])
    assert result.exit_code == 0


def test_explore_excludes_empty():
    result = runner.invoke(app, ['explore', '-g', '-x', '', str(GUESS_FIXTURE)])
    assert result.exit_code == 0
