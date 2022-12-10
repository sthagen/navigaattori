import pathlib

from typer.testing import CliRunner

import navigaattori
from navigaattori.cli import app

runner = CliRunner()

BASIC_FIXTURE = pathlib.Path('test') / 'fixtures' / 'basic'


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
