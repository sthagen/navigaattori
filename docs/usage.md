# Usage

## Help

```console
❯ navigaattori
Usage: navigaattori [OPTIONS] COMMAND [ARGS]...

  Navigator (Finnish: navigaattori) guided by conventions.

Options:
  -V, --version  Display the application version and exit
  -h, --help     Show this message and exit.

Commands:
  explore  Verify the structure definition against the file system.
  version  Display the application version and exit.
```
## Version

```console
❯ navigaattori version
Navigator (Finnish: navigaattori) guided by conventions. version 2022.12.10+parent.50b514b6
```

### Version - Help

```console
❯ navigaattori version --help
Usage: navigaattori version [OPTIONS]

  Display the application version and exit.

Options:
  -h, --help  Show this message and exit.
```

## Explore

```console
❯ navigaattori explore basic 2>&1 | cut -c34- | sed "s/NAVIGAATTORI/.../g; s/WARNING/W/g; s/ERROR/E/g; s/INFO/I/g;"
I [...]: screening target type (wun) ...
I [...]: screening target type (bar) ...
E [...]: spec_path file (basic/bar/structure.yml) for target type (bar) does not exist or is empty
I [...]: assessing target type (wun) ...
I [...]: - assessing target (foo_kind) with target type (wun) ...
E [...]:   + invalid (approvals) resource (approvals.yml) for facet (default) of target (foo_kind) with target type (wun) - resource does not exist or is no file
E [...]:   + invalid (bind) resource (bind.txt) for facet (default) of target (foo_kind) with target type (wun) - resource does not exist or is no file
E [...]:   + invalid (changes) resource (changes.yml) for facet (default) of target (foo_kind) with target type (wun) - resource does not exist or is no file
E [...]:   + invalid (meta) resource (meta-default.yml) for facet (default) of target (foo_kind) with target type (wun) - resource does not exist or is no file
I [...]: skipping invalid target (bar)
I [...]: reporting target type (wun) ...
I [...]: - target_type='wun':
I [...]:   + dir -> foo
I [...]:   + file -> structure.yml
I [...]:   + structure =>
I [...]:     * foo_kind =>
I [...]:       - default =>
I [...]:         + approvals -> approvals.yml
I [...]:         + bind -> bind.txt
I [...]:         + changes -> changes.yml
I [...]:         + meta -> meta-default.yml
I [...]:         + render -> True
I [...]:         + formats -> ['html', 'pdf']
I [...]:         + options -> None
I [...]:   + valid -> False
I [...]: reporting target type (bar) ...
I [...]: - target_type='bar':
I [...]:   + dir -> bar
I [...]:   + file -> structure.yml
I [...]:   + structure -> {}
I [...]:   + valid -> False
W [...]: ['approvals', 'bind', 'changes', 'meta', 'render', 'formats', 'options']
E [...]: specifications for target types (bar, wun) are invalid
```

### Explore - Help

```console
❯ navigaattori explore --help
Usage: navigaattori explore [OPTIONS] [DOC_ROOT_POS]

  Verify the structure definition against the file system.

Arguments:
  [DOC_ROOT_POS]

Options:
  -d, --document-root TEXT  Root of the document tree to visit. Optional
                            (default: positional tree root value)
  -v, --verbose             Verbose output (default is False)
  -s, --strict              Ouput noisy warnings on console (default is False)
  -h, --help                Show this message and exit.
```
