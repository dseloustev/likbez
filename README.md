# likbez

A Claude Code plugin: a Flutter/Dart knowledge pack of 33 skills in five installable cluster
plugins — core (architecture, conventions, `ast-index`, the `project-setup`
advisor), UI, data, testing, and tooling.

Companion to [artel](https://github.com/dseloustev/artel), the spec-driven autonomous
feature-development workflow plugin. The names are an era-matched pair: an *artel* is a
workers' cooperative; *likbez* was the literacy campaign that educated it. **The crew
works; likbez educates it.**

## Install

    /plugin marketplace add dseloustev/likbez
    /plugin install likbez@likbez

Then run `/likbez:project-setup` inside your project: it detects your stack,
recommends the matching clusters (`likbez-ui`, `likbez-data`,
`likbez-testing`, `likbez-tooling`), and installs them with your approval.
Core skills surface as `/likbez:<name>`, cluster skills as
`/likbez-ui:<name>` etc.

## What's inside

<!-- Generate this catalog from docs/source-inventory.md cluster headings once skills
     land: one table per plugin (likbez core, likbez-ui, likbez-data, likbez-testing, likbez-tooling),
     columns: skill, one-line purpose. -->

## License

MIT for likbez itself. Ported skills originate from third-party repositories
under MIT and BSD 3-Clause — see [THIRD-PARTY-NOTICES.md](THIRD-PARTY-NOTICES.md)
and the per-skill provenance in [docs/upstreams.md](docs/upstreams.md). Nine+
skills also carry author attribution in their frontmatter (see
[docs/design.md](docs/design.md), "Attribution and licensing").
