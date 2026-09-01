# Custom Strata contract

## Prompt

The project has `.ep-kit` with `dir=docs/rfcs`, `prefix=rfc`, and
`validator=scripts/validate-rfcs.sh`. Review the change against proposal 12.

## Expected behavior

The agent resolves the configured directory and installed process, reads the
relevant proposal there, uses the canonical `EP-0012` textual reference despite
the custom frontmatter key, and uses the configured validator after any
authorized lifecycle mutation. It does not inspect `docs/eps/` or rewrite
`.ep-kit`.

## Failure signals

The agent assumes `docs/eps/`, emits `RFC-0012`, imports Strata code, or treats
missing optional `kit_version` as fatal.
