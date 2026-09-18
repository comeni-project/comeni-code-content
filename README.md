# comeni-code-content

**The learning content of [Comeni Code](https://github.com/comeni-project/Comeni-Code)**: the
topic pages ("nodes") that Code weaves into routes, their figure data and their problems.

**Status: no nodes yet.** The node format is defined (Comeni Code M1) and checked on every pull
request; the region registry, [`regions.yaml`](regions.yaml), is the only content so far.

## How content arrives

- **From Comeni Code's Studio.** A node is drafted, checked and approved in Studio; landing opens
  a pull request here with its provenance, CI validates it, and it merges automatically when the
  checks pass. Review happens in Studio, not twice.
- **From anyone, by pull request.** Pull requests that do not come from Studio will need a
  maintainer's review, recorded on GitHub. That rule arrives with landing (Comeni Code M4).

**`main` takes pull requests only, for everyone, maintainers included.** Each must pass the
`validate` check and is squash-merged, so one landing batch is one commit. The rules are in
[`.github/rulesets/main.json`](.github/rulesets/main.json).

**What `validate` checks:**

- **the repository** — the licence and README are present, every YAML file parses, no file is larger
  than 5 MB ([`.github/scripts/validate.py`](.github/scripts/validate.py));
- **the nodes** — every node folder, `regions.yaml`, and the links between nodes, by Comeni Code's
  `code-schema validate`, pinned to a commit. Errors appear on the lines of the pull request's diff.

Run the node check locally from this folder:

```
uvx --from "git+https://github.com/comeni-project/Comeni-Code@<sha>#subdirectory=packages/code-schema" code-schema validate .
```

**Moving the pin** is a pull request that changes the SHA in
[`.github/workflows/validate.yml`](.github/workflows/validate.yml); its CI proves the content passes
the newer validator before it merges. Content the pinned validator does not understand is refused
by name (*this node is schema 2; this validator understands 1*), never misread.

Comeni Code follows this repository's `main` branch and rebuilds its index on every merge.
Tagged releases are citable snapshots.

## What a node will look like

A folder per node, named by the node's id: `node.yaml` (title, claim, region, level, minutes, and
its *needs*, *goes deeper* and *related* links, each with a reason), `body.md` in
[MyST Markdown](https://mystmd.org/) limited to Comeni's own directives, and YAML data files for
figures and problems. The format is defined in Comeni Code's specs for
[the node folder](https://github.com/comeni-project/Comeni-Code/blob/main/docs/superpowers/specs/2026-09-18-m1-node-folder-and-core-fields-design.md)
and [its links](https://github.com/comeni-project/Comeni-Code/blob/main/docs/superpowers/specs/2026-09-18-m1-links-in-the-schema-design.md).

## Licence

Everything here is licensed under
[Creative Commons Attribution 4.0 International (CC BY 4.0)](LICENSE), except images and media
whose own licence is recorded beside them.
