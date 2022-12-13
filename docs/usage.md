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
  explore  Explore the structures definition tree in the file system.
  version  Display the application version and exit.
```
## Version

```console
❯ navigaattori version
Navigator (Finnish: navigaattori) guided by conventions. version 2022.12.12+parent.36405dcb
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
I [...]: - will exclude (.git/, render/pdf/) path partials
I [...]: not guessing but reading target types from (basic/structures.yml) data instead ...
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
E [...]: specifications for target types (bar, wun) are invalid
```

using different excludes than the defaults `.git/` and `render/pdf/`:

```console
❯ navigaattori explore basic --excludes foo,bar 2>&1 | cut -c34- | sed "s/NAVIGAATTORI/.../g; s/WARNING/W/g; s/ERROR/E/g; s/INFO/I/g;"
I [...]: - will exclude (foo, bar) path partials
I [...]: not guessing but reading target types from (basic/structures.yml) data instead ...
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
E [...]: specifications for target types (bar, wun) are invalid
```

missing structures file (the folder name lowercase guess is maybe not optimal ...):

```console
❯ navigaattori explore guess 2>&1 | cut -c34- | sed "s/NAVIGAATTORI/.../g; s/WARNING/W/g; s/ERROR/E/g; s/INFO/I/g;"
I [...]: - will exclude (.git/, render/pdf/) path partials
E [...]: structures file (guess/structures.yml) does not exist or is empty
I [...]: ... you may want to try the --guess option to the explore command to bootstrap a structures file
E [...]: target types are not present - invalid structures file?
```

taking the hint and enter guess-mode:

```console
❯ navigaattori explore guess --guess 2>&1 | cut -c34- | sed "s/NAVIGAATTORI/.../g; s/WARNING/W/g; s/ERROR/E/g; s/INFO/I/g;"
I [...]: - will exclude (.git/, render/pdf/) path partials
W [...]: structures file (guess/structures.yml) does not exist or is empty
I [...]: guessing target types from recursive search for (structure.yml) files ...
I [...]: - guessed target type (foo) from path (guess/foo/structure.yml)
I [...]: screening target type (foo) ...
I [...]: assessing target type (foo) ...
I [...]: - assessing target (foo_kind) with target type (foo) ...
I [...]: assessing approvals (guess/foo/approvals.yml) yielding:
I [...]: approvals sequence loaded 3 approvals from (guess/foo/approvals.yml):
I [...]: - {'role': 'Author', 'name': 'An Author'}
I [...]: - {'role': 'Review', 'name': 'A Reviewer'}
I [...]: - {'role': 'Approved', 'name': 'An App Rover'}
I [...]: approvals sequence successfully loaded from (guess/foo/approvals.yml):
I [...]: sequence of approvals from (guess/foo/approvals.yml) is valid
I [...]: assessing binder (guess/foo/bind.txt) yielding:
I [...]: binder sequence loaded 1 resource from (guess/foo/bind.txt):
I [...]: - empty.md
I [...]: binder sequence successfully loaded from (guess/foo/bind.txt):
I [...]: - resource (empty.md) points to file (at guess/foo/empty.md)
I [...]: sequence of resources of (guess/foo/bind.txt) is valid
I [...]: assessing changes (guess/foo/changes.yml) yielding:
I [...]: changes sequence loaded 2 changes from (guess/foo/changes.yml):
I [...]: - {'author': 'An Author', 'date': 'PUBLICATIONDATE', 'issue': '01', 'revision': '00', 'summary': 'Initial Issue'}
I [...]: - {'author': 'An Author', 'date': '', 'issue': '01', 'revision': '01', 'summary': 'Fixed a nit'}
I [...]: changes sequence successfully loaded from (guess/foo/changes.yml):
I [...]: sequence of changes from (guess/foo/changes.yml) is valid
I [...]: assessing changes (guess/foo/meta-default.yml) yielding:
I [...]: top level metadata successfully loaded from (guess/foo/meta-default.yml):
I [...]: reporting current metadata starting from (guess/foo/meta-default.yml) ...
I [...]: - document =>
I [...]:   + import -> meta-base.yml
I [...]:   + patch =>
I [...]:     * header_id -> P99999
I [...]:     * header_date -> PUBLICATIONDATE
I [...]:     * toc_level -> 3
I [...]:     * list_of_figures ->
I [...]:     * list_of_tables ->
I [...]: - trying to import metadata from (guess/foo/meta-base.yml)
I [...]: metadata successfully loaded completely starting from (guess/foo/meta-default.yml):
I [...]: reporting current metadata starting from (guess/foo/meta-default.yml) ...
I [...]: - document =>
I [...]:   + common =>
I [...]:     * title -> Ttt Tt Tt
I [...]:     * header_title -> Ttt Tt
I [...]:     * sub_title -> The Deep Spec
I [...]:     * header_type -> Engineering Document
I [...]:     * header_id -> P99999
I [...]:     * issue -> 01
I [...]:     * revision -> 00
I [...]:     * header_date -> PUBLICATIONDATE
I [...]:     * header_issue_revision_combined -> None
I [...]:     * footer_frame_note -> VERY CONSEQUENTIAL
I [...]:     * footer_page_number_prefix -> Page
I [...]:     * change_log_issue_label -> Iss.
I [...]:     * change_log_revision_label -> Rev.
I [...]:     * change_log_date_label -> Date
I [...]:     * change_log_author_label -> Author
I [...]:     * change_log_description_label -> Description
I [...]:     * approvals_role_label -> Approvals
I [...]:     * approvals_name_label -> Name
I [...]:     * approvals_date_and_signature_label -> Date and Signature
I [...]:     * proprietary_information -> /opt/legal/proprietary_information.txt
I [...]:     * toc_level -> 3
I [...]:     * list_of_figures ->
I [...]:     * list_of_tables ->
I [...]:     * font_path -> /opt/fonts/
I [...]:     * font_suffix -> .otf
I [...]:     * bold_font -> ITCFranklinGothicStd-Demi
I [...]:     * italic_font -> ITCFranklinGothicStd-BookIt
I [...]:     * bold_italic_font -> ITCFranklinGothicStd-DemiIt
I [...]:     * main_font -> ITCFranklinGothicStd-Book
I [...]:     * fixed_font_package -> sourcecodepro
I [...]:     * code_fontsize -> \scriptsize
I [...]:     * chosen_logo -> /opt/logo/liitos-logo.png
I [...]: metadata from (guess/foo/meta-default.yml) seems to be valid
I [...]: reporting target type (foo) ...
I [...]: - target_type='foo':
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
I [...]:   + valid -> True
I [...]: structures appear to be valid (on file system screening level)
I [...]: dumping proposed global expanded file from guessing to (GUESSED_STRUCTURES/tree.yml) ...
I [...]: dumping proposed structures file from guessing to (GUESSED_STRUCTURES/structures.yml) ...
```

Inspecting folder `GUESSED_STRUCTURES` contents:

```console
❯ bat --plain GUESSED_STRUCTURES/structures.yml
structures:
  foo: foo/structure.yml
```

... and:

```console
❯ bat --plain GUESSED_STRUCTURES/tree.yml
structures:
  foo:
    dir: foo
    file: structure.yml
    structure:
      foo_kind:
        default:
          approvals: approvals.yml
          bind: bind.txt
          changes: changes.yml
          formats:
          - html
          - pdf
          meta: meta-default.yml
          options: null
          render: true
    valid: true
```

### Explore - Help

```console
❯ navigaattori explore --help
Usage: navigaattori explore [OPTIONS] [DOC_ROOT_POS]

  Explore the structures definition tree in the file system.

Arguments:
  [DOC_ROOT_POS]

Options:
  -d, --document-root TEXT  Root of the document tree to visit. Optional
                            (default: positional tree root value)
  -v, --verbose             Verbose output (default is False)
  -s, --strict              Output noisy warnings on console (default is
                            False)
  -g, --guess               Guess and derive structures from folder tree
                            structure.yml files if possible (default is False)
  -x, --excludes TEXT       comma separated list of values to exclude paths
                            containing the substring (default:
                            .git/,render/pdf/)  [default: .git/,render/pdf/]
  -h, --help                Show this message and exit.
```
