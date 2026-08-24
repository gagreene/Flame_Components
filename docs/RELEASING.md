# Release Procedure

This describes how to cut a release of `flame-components` once Trusted Publishing is
configured (one-time setup below). It does not need updating for each release — it
describes the current process, not a specific release's history.

## One-time setup (do this once, before the first automated publish)

These steps require the PyPI/TestPyPI web UI and GitHub repository settings — they can't
be automated from a local session.

1. **GitHub environments.** In the repo's Settings → Environments, create `pypi` and
   `testpypi`. Add a required reviewer to `pypi` (manual approval before every production
   publish); `testpypi` can be left unprotected since nothing it touches is a real release.
2. **Trusted Publishers.** On both [pypi.org](https://pypi.org/manage/account/publishing/)
   and [test.pypi.org](https://test.pypi.org/manage/account/publishing/), register a
   *pending* trusted publisher (the project doesn't need to exist yet) with:
   - Owner: `gagreene`, Repository: `flame_components`
   - Workflow name: `release.yml`
   - Environment name: `pypi` (on pypi.org) / `testpypi` (on test.pypi.org) — must match
     the `environment:` name in `.github/workflows/release.yml` exactly.
3. Branch protection on `master` (Phase 6 of the readiness plan) — require the `Tests`
   workflow's checks to pass before merge.

## Cutting a release

1. Make sure `master` is green (the `Tests` workflow passing on the latest commit) and the
   worktree is clean.
2. Decide the version. hatch-vcs derives it entirely from the git tag — never edit a
   version number by hand anywhere.
3. Create and push an annotated tag:
   ```bash
   git tag -a v0.1.1 -m "v0.1.1"
   git push origin v0.1.1
   ```
   For a TestPyPI rehearsal first, use a release-candidate tag instead, e.g. `v0.1.1rc1`.
4. Create a GitHub Release from that tag (Releases → Draft a new release), with curated
   user-facing notes (see "What goes in release notes" below).
   - **Mark it as a pre-release** for an `rcN` tag → publishing this Release triggers
     `.github/workflows/release.yml`'s `publish-testpypi` job.
   - **Leave it as a full release** for a real version tag → triggers `publish-pypi`.
5. Publishing the Release triggers the workflow automatically: it builds the wheel and
   sdist, runs `twine check`, installs the wheel into a fresh environment and runs
   `scripts/smoke_test.py`, attaches both files to the GitHub Release, then waits for the
   `pypi` (or `testpypi`) environment's required approval before actually uploading.
6. Approve the environment deployment when GitHub prompts for it. This is the last chance
   to stop a bad release before it's public.
7. After it completes, verify: `pip install flame-components==<version>` in a clean
   environment, then `python -c "import flame_components as fc; print(fc.__version__)"`.

## What goes in release notes

Only externally meaningful information: new features, behavior changes, compatibility
changes, deprecations/removals, and fixes that could affect users. Internal
implementation cleanup, test-suite restructuring, and detailed bug-discovery narrative
belong in the private Obsidian vault's Decision Log, not here.

## If something goes wrong

PyPI files and version numbers **cannot be replaced or re-uploaded** — once a version is
public, that exact set of bytes is permanent (even if deleted, the version number can
never be reused). Options for a broken release:

- **Yank it** (PyPI project page → Manage → yank a release) if it's broken enough that
  people shouldn't install it, but a small number of people already have working pins to
  it. A yanked release stays downloadable by exact version pin but is hidden from normal
  resolution.
- **Ship a new patch version** with the fix. This is the normal path for almost anything —
  there is no "fix in place."
- If the *tag* was wrong (pointed at the wrong commit) but nothing was published yet,
  it's fine to delete and recreate the tag — see the Decision Log's `v0.1.0` re-pointing
  entry for a precedent. Once something has actually been published to PyPI under that
  version, don't re-point the tag; cut a new version instead.
