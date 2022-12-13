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
  eject    Eject a template.
  explore  Explore the structures definition tree in the file system.
  version  Display the application version and exit.
```
## Version

```console
❯ navigaattori version
Navigator (Finnish: navigaattori) guided by conventions. version 2022.12.13+parent.ff7049ef
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
I [...]: loading liitos vocabulary from (templates/liitos_vocabulary.yml) ...
I [...]: dumping liitos vocabulary to (liitos-vocabulary.yml) ...
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
I [...]: verifying metadata starting from (guess/foo/meta-default.yml) uses only tokens from the liitos vocabulary ...
I [...]: metadata successfully verified 32 tokens (82.05% of vocabulary)
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

## Eject

```console
❯ navigaattori eject
2022-12-13T20:58:36.347693+00:00 ERROR [NAVIGAATTORI]: eject of template with no name requested
2022-12-13T20:58:36.348226+00:00 INFO [NAVIGAATTORI]: templates known: (liitos-vocabulary-yaml)
```

indicating the source:

```console
❯ navigaattori eject l
---
slot_marker: VALUE.SLOT
targets:
  title:
    eol_marker: '%%_PATCH_%_MAIN_%_TITLE_%%'
    default: null
    scope: metadata.tex.in
  sub_title:
    eol_marker: '%%_PATCH_%_SUB_%_TITLE_%%'
    default: ' '
    scope: metadata.tex.in
  header_title:
    eol_marker: '%%_PATCH_%_HEADER_%_TITLE_%%'
    default: null
    scope: metadata.tex.in
  header_type:
    eol_marker: '%%_PATCH_%_TYPE_%%'
    default: Engineering Document
    scope: metadata.tex.in
  header_id:
    eol_marker: '%%_PATCH_%_ID_%%'
    default: null
    scope: metadata.tex.in
  header_id_label:
    eol_marker: '%%_PATCH_%_ID_%_LABEL_%%'
    default: 'Doc. ID:'
    scope: metadata.tex.in
  header_id_show:
    eol_marker: '%%_PATCH_%_ID_%_SHOW_%%'  # dummy to support inversion
    default: true
    scope: metadata.tex.in
  issue:
    eol_marker: '%%_PATCH_%_ISSUE_%%'
    default: '01'
    scope: metadata.tex.in
  revision:
    eol_marker: '%%_PATCH_%_REVISION_%%'
    default: '00'
    scope: metadata.tex.in
  header_issue_revision_combined:
    eol_marker: '%%_PATCH_%_ISSUE_%_REVISION_%_COMBINED_%%'
    default: Iss \theMetaIssCode, Rev \theMetaRevCode
    scope: metadata.tex.in
  header_issue_revision_combined_label:
    eol_marker: '%%_PATCH_%_ISSUE_%_REVISION_%_COMBINED_%_LABEL_%%'
    default: 'Issue, Revision:'
    scope: metadata.tex.in
  header_issue_revision_combined_show:
    eol_marker: '%%_PATCH_%_ISSUE_%_REVISION_%_COMBINED_%_SHOW_%%'  # dummy to support inversion
    default: true
    scope: metadata.tex.in
  header_date:
    eol_marker: '%%_PATCH_%_DATE_%%'
    default: null
    scope: metadata.tex.in
  header_date_label:
    eol_marker: '%%_PATCH_%_DATE_%_LABEL%%'
    default: 'Date:'
    scope: metadata.tex.in
  header_date_enable_auto:
    eol_marker: '%%_PATCH_%_DATE_%_ENABLE_%_AUTO_%%'  # dummy to support inversion
    default: true
    scope: metadata.tex.in
  header_date_show:
    eol_marker: '%%_PATCH_%_DATE_%_SHOW_%%'  # dummy to support inversion
    default: true
    scope: metadata.tex.in
  footer_frame_note:
    eol_marker: '%%_PATCH_%_FRAME_%_NOTE_%%'
    default: null
    scope: metadata.tex.in
  footer_page_number_prefix:
    eol_marker: '%%_PATCH_%_FOOT_%_PAGE_%_COUNTER_%_LABEL_%%'
    default: 'Page'
    scope: metadata.tex.in
  change_log_issue_label:
    eol_marker: '%%_PATCH_%_CHANGELOG_%_ISSUE_%_LABEL_%%'
    default: 'Iss.'
    scope: metadata.tex.in
  change_log_revision_label:
    eol_marker: '%%_PATCH_%_CHANGELOG_%_REVISION_%_LABEL_%%'
    default: 'Rev.'
    scope: metadata.tex.in
  change_log_date_label:
    eol_marker: '%%_PATCH_%_CHANGELOG_%_DATE_%_LABEL_%%'
    default: 'Date'
    scope: metadata.tex.in
  change_log_author_label:
    eol_marker: '%%_PATCH_%_CHANGELOG_%_AUTHOR_%_LABEL_%%'
    default: Author
    scope: metadata.tex.in
  change_log_description_label:
    eol_marker: '%%_PATCH_%_CHANGELOG_%_DESCRIPTION_%_LABEL_%%'
    default: Description
    scope: metadata.tex.in
  approvals_role_label:
    eol_marker: '%%_PATCH_%_APPROVALS_%_ROLE_%_LABEL_%%'
    default: Approvals
    scope: metadata.tex.in
  approvals_name_label:
    eol_marker: '%%_PATCH_%_APPROVALS_%_NAME_%_LABEL_%%'
    default: Name
    scope: metadata.tex.in
  approvals_date_and_signature_label:
    eol_marker: '%%_PATCH_%_APPROVALS_%_DATE_%_AND_%_SIGNATURE_%_LABEL_%%'
    default: Date and Signature
    scope: metadata.tex.in
  proprietary_information:
    eol_marker: '%%_PATCH_%_PROPRIETARY_%_INFORMATION_%_LABEL_%%'
    default: null
    scope: metadata.tex.in
  toc_level:
    eol_marker: '%%_PATCH_%_TOC_%_LEVEL_%%'
    default: 2
    scope: driver.tex.in
  list_of_figures:
    eol_marker: '%%_PATCH_%_LOF_%%'
    default: '%'  # empty string to enable lof
    scope: driver.tex.in
  list_of_tables:
    eol_marker: '%%_PATCH_%_LOT_%%'
    default: '%'  # empty string to enable lot
    scope: driver.tex.in
  font_path:
    eol_marker: '%%_PATCH_%_FONT_%_PATH_%%'
    default: /opt/fonts/
    scope: setup.tex.in
  font_suffix:
    eol_marker: '%%_PATCH_%_FONT_%_SUFFIX_%%'
    default: .otf
    scope: setup.tex.in
  bold_font:
    eol_marker: '%%_PATCH_%_BOLD_%_FONT_%%'
    default: ITCFranklinGothicStd-Demi
    scope: setup.tex.in
  italic_font:
    eol_marker: '%%_PATCH_%_ITALIC_%_FONT_%%'
    default: ITCFranklinGothicStd-BookIt
    scope: setup.tex.in
  bold_italic_font:
    eol_marker: '%%_PATCH_%_BOLDITALIC_%_FONT_%%'
    default: ITCFranklinGothicStd-DemiIt
    scope: setup.tex.in
  main_font:
    eol_marker: '%%_PATCH_%_MAIN_%_FONT_%%'
    default: ITCFranklinGothicStd-Book
    scope: setup.tex.in
  fixed_font_package:
    eol_marker: '%%_PATCH_%_FIXED_%_FONT_%_PACKAGE_%%'
    default: sourcecodepro
    scope: setup.tex.in
  code_fontsize:
    eol_marker: '%%_PATCH_%_CODE_%_FONTSIZE_%%'
    default: \scriptsize
    scope: setup.tex.in
  chosen_logo:
    eol_marker: '%%_PATCH_%_CHOSEN_%_LOGO_%%'
    default: liitos-logo.png
    scope: setup.tex.in
tokens:
  '%%_PATCH_%_MAIN_%_TITLE_%%': title
  '%%_PATCH_%_SUB_%_TITLE_%%': sub_title
  '%%_PATCH_%_HEADER_%_TITLE_%%': header_title
  '%%_PATCH_%_TYPE_%%': header_type
  '%%_PATCH_%_ID_%%': header_id
  '%%_PATCH_%_ID_%_LABEL_%%': header_id_label
  '%%_PATCH_%_ID_%_SHOW_%%': header_id_show  # dummy to support inversion
  '%%_PATCH_%_ISSUE_%%': issue
  '%%_PATCH_%_REVISION_%%': revision
  '%%_PATCH_%_ISSUE_%_REVISION_%_COMBINED_%%': header_issue_revision_combined
  '%%_PATCH_%_ISSUE_%_REVISION_%_COMBINED_%_LABEL_%%': header_issue_revision_combined_label
  '%%_PATCH_%_ISSUE_%_REVISION_%_COMBINED_%_SHOW_%%': header_issue_revision_combined_show  # dummy to support inversion
  '%%_PATCH_%_DATE_%%': header_date
  '%%_PATCH_%_DATE_%_ENABLE_%_AUTO__%%': header_date_enable_auto  # dummy to support inversion
  '%%_PATCH_%_DATE_%_LABEL_%%': header_date_label
  '%%_PATCH_%_DATE_%_SHOW_%%': header_date_show  # dummy to support inversion
  '%%_PATCH_%_FRAME_%_NOTE_%%': footer_frame_note
  '%%_PATCH_%_FOOT_%_PAGE_%_COUNTER_%_LABEL_%%': footer_page_number_prefix
  '%%_PATCH_%_CHANGELOG_%_ISSUE_%_LABEL_%%': change_log_issue_label
  '%%_PATCH_%_CHANGELOG_%_REVISION_%_LABEL_%%': change_log_revision_label
  '%%_PATCH_%_CHANGELOG_%_DATE_%_LABEL_%%': change_log_date_label
  '%%_PATCH_%_CHANGELOG_%_AUTHOR_%_LABEL_%%': change_log_author_label
  '%%_PATCH_%_CHANGELOG_%_DESCRIPTION_%_LABEL_%%': change_log_description_label
  '%%_PATCH_%_APPROVALS_%_ROLE_%_LABEL_%%': approvals_role_label
  '%%_PATCH_%_APPROVALS_%_NAME_%_LABEL_%%': approvals_name_label
  '%%_PATCH_%_APPROVALS_%_DATE_%_AND_%_SIGNATURE_%_LABEL_%%': approvals_date_and_signature_label
  '%%_PATCH_%_PROPRIETARY_%_INFORMATION_%_LABEL_%%': proprietary_information
  '%%_PATCH_%_TOC_%_LEVEL_%%': toc_level
  '%%_PATCH_%_LOF_%%': list_of_figures
  '%%_PATCH_%_LOT_%%': list_of_tables
  '%%_PATCH_%_FONT_%_PATH_%%': font_path
  '%%_PATCH_%_FONT_%_SUFFIX_%%': font_suffix
  '%%_PATCH_%_BOLD_%_FONT_%%': bold_font
  '%%_PATCH_%_ITALIC_%_FONT_%%': italic_font
  '%%_PATCH_%_BOLDITALIC_%_FONT_%%': bold_italic_font
  '%%_PATCH_%_MAIN_%_FONT_%%': main_font
  '%%_PATCH_%_FIXED_%_FONT_%_PACKAGE_%%': fixed_font_package
  '%%_PATCH_%_CODE_%_FONTSIZE_%%': code_fontsize
  '%%_PATCH_%_CHOSEN_%_LOGO_%%': chosen_logo

```

to a name path:

```console
❯ navigaattori eject l -o a-name.yml
2022-12-13T21:00:01.948022+00:00 WARNING [NAVIGAATTORI]: requested writing (templates/liitos_vocabulary.yml) to file (a-name.yml)
```

```console
❯ head a-name.yml
---
slot_marker: VALUE.SLOT
targets:
  title:
    eol_marker: '%%_PATCH_%_MAIN_%_TITLE_%%'
    default: null
    scope: metadata.tex.in
  sub_title:
    eol_marker: '%%_PATCH_%_SUB_%_TITLE_%%'
    default: ' '
```

### Eject - Help

```console
❯ navigaattori eject --help
Usage: navigaattori eject [OPTIONS] [THAT]

  Eject a template. Enter unique part to retrieve, any unknown word to obtain
  the list of known templates.

Arguments:
  [THAT]

Options:
  -o, --output-path TEXT  Path to output unambiguous content to - like when
                          ejecting a template
  -h, --help              Show this message and exit.

```
