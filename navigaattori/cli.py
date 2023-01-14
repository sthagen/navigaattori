"""Command line interface for navigator (Finnish: navigaattori) guided by conventions."""
import datetime as dti
import logging
import pathlib
import sys

import typer

import navigaattori.api as api
import navigaattori.eject as eje
from navigaattori import (
    APP_NAME,
    DEFAULT_STRUCTURE_NAME,
    QUIET,
    TS_FORMAT_PAYLOADS,
    __version__ as APP_VERSION,
    log,
)

app = typer.Typer(
    add_completion=False,
    context_settings={'help_option_names': ['-h', '--help']},
    no_args_is_help=True,
)

DocumentRoot = typer.Option(
    '',
    '-d',
    '--document-root',
    help='Root of the document tree to visit. Optional\n(default: positional tree root value)',
)
StructureName = typer.Option(
    DEFAULT_STRUCTURE_NAME,
    '-s',
    '--structure',
    help='structure mapping file (default: {gat.DEFAULT_STRUCTURE_NAME})',
)
TargetName = typer.Option(
    '',
    '-t',
    '--target',
    help='target document key',
)
FacetName = typer.Option(
    '',
    '-f',
    '--facet',
    help='facet key of target document',
)
Verbosity = typer.Option(
    False,
    '-v',
    '--verbose',
    help='Verbose output (default is False)',
)
Strictness = typer.Option(
    False,
    '-s',
    '--strict',
    help='Output noisy warnings on console (default is False)',
)
Guess = typer.Option(
    False,
    '-g',
    '--guess',
    help='Guess and derive structures from folder tree structure.yml files if possible (default is False)',
)
OutputPath = typer.Option(
    '',
    '-o',
    '--output-path',
    help='Path to output unambiguous content to - like when ejecting a template',
)
Excludes = typer.Option(
    '.git/,render/pdf/',
    '-x',
    '--excludes',
    help='comma separated list of values to exclude paths\ncontaining the substring (default: .git/,render/pdf/)',
)


@app.callback(invoke_without_command=True)
def callback(
    version: bool = typer.Option(
        False,
        '-V',
        '--version',
        help='Display the application version and exit',
        is_eager=True,
    )
) -> None:
    """
    Navigator (Finnish: navigaattori) guided by conventions.
    """
    if version:
        typer.echo(f'{APP_NAME} version {APP_VERSION}')
        raise typer.Exit()


def _verify_call_vector(
    doc_root: str,
    doc_root_pos: str,
    verbose: bool,
    strict: bool,
    guess: bool,
    excludes: str,
) -> tuple[int, str, str, dict[str, object]]:
    """DRY"""
    doc = doc_root.strip()
    if not doc and doc_root_pos:
        doc = doc_root_pos
    if not doc:
        print('Document tree root required', file=sys.stderr)
        return 2, 'Document tree root required', '', {}

    doc_root_path = pathlib.Path(doc)
    if doc_root_path.exists():
        if not doc_root_path.is_dir():
            print(f'requested tree root at ({doc}) is not a folder', file=sys.stderr)
            return 2, f'requested tree root at ({doc}) is not a folder', '', {}
    else:
        print(f'requested tree root at ({doc}) does not exist', file=sys.stderr)
        return 2, f'requested tree root at ({doc}) does not exist', '', {}

    options = {
        'quiet': QUIET and not verbose and not strict,
        'strict': strict,
        'verbose': verbose,
        'guess': guess,
        'excludes': excludes,
    }
    if verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    return 0, '', doc, options


@app.command('explore')
def explore(  # noqa
    doc_root_pos: str = typer.Argument(''),
    doc_root: str = DocumentRoot,
    verbose: bool = Verbosity,
    strict: bool = Strictness,
    guess: bool = Guess,
    excludes: str = Excludes,
) -> int:
    """
    Explore the structures definition tree in the file system.
    """
    code, message, doc, options = _verify_call_vector(doc_root, doc_root_pos, verbose, strict, guess, excludes)
    if code:
        log.error(message)
        return sys.exit(code)

    start_time = dti.datetime.now(tz=dti.timezone.utc)
    start_ts = start_time.strftime(TS_FORMAT_PAYLOADS)
    log.info(f'start timestamp ({start_ts})')

    code, _ = api.explore(doc_root=doc, options=options)

    end_time = dti.datetime.now(tz=dti.timezone.utc)
    end_ts = end_time.strftime(TS_FORMAT_PAYLOADS)
    duration_secs = (end_time - start_time).total_seconds()
    log.info(f'end timestamp ({end_ts})')
    log.info(f'explored structures at {doc} in {duration_secs} secs')
    return sys.exit(code)


@app.command('eject')
def eject(  # noqa
    that: str = typer.Argument(''),
    out: str = OutputPath,
) -> int:
    """
    Eject a template. Enter unique part to retrieve, any unknown word to obtain the list of known templates.
    """
    return sys.exit(eje.this(thing=that, out=out))


@app.command('version')
def app_version() -> None:
    """
    Display the application version and exit.
    """
    callback(True)
