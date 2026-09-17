# comeni-code-content

**The learning content of [Comeni Code](https://github.com/comeni-project/Comeni-Code)**: the
topic pages ("nodes") that Code weaves into routes, their figure data and their problems.

**Status: empty.** The node format is being defined in Comeni Code's first content phase (M1).
Until then this repository holds only its licence.

## How content arrives

- **From Comeni Code's Studio.** A node is drafted, checked and approved in Studio; landing opens
  a pull request here with its provenance, CI validates it, and it merges automatically when the
  checks pass. Review happens in Studio, not twice.
- **From anyone, by pull request.** Pull requests that do not come from Studio will need a
  maintainer's review, recorded on GitHub. That rule arrives with landing (Comeni Code M4).

**`main` takes pull requests only, for everyone, maintainers included.** Each must pass the
`validate` check and is squash-merged, so one landing batch is one commit. The rules are in
[`.github/rulesets/main.json`](.github/rulesets/main.json).

**What `validate` checks today:** the licence and README are present, every YAML file parses, and
no file is larger than 5 MB. Node validation arrives with Comeni Code's M1 phase.

Comeni Code follows this repository's `main` branch and rebuilds its index on every merge.
Tagged releases are citable snapshots.

## What a node will look like

A folder per node: `node.yaml` (its claim, what it needs and why, related topics, provenance),
`body.md` in [MyST Markdown](https://mystmd.org/) limited to Comeni's own directives, and YAML data
files for figures and problems. The exact fields are defined in Comeni Code's M1 phase — see its
[architecture spec](https://github.com/comeni-project/Comeni-Code/blob/main/docs/superpowers/specs/2026-09-17-comeni-code-architecture-and-roadmap-design.md).

## Licence

Everything here is licensed under
[Creative Commons Attribution 4.0 International (CC BY 4.0)](LICENSE), except images and media
whose own licence is recorded beside them.
