# Verification scope

## Baseline

- Upstream: `https://github.com/bradygaster/squad`
- Release: `v1.1.0`
- Commit: `c24da2aad2ab7576f6b68dec2bc50b2fe2dc7a8a`
- Upstream license: MIT.

The baseline source inventory contains 145 published-document source files and 30 additional specification, feature, internal-specification, migration, and overview files. `coverage.csv` maps these 175 files to the manuscript.

## Squad 2.0 documentation rescan

- Preview baseline: `v2.0.0-preview.2`, commit `481c944596abfa2053e2acd88d765639f994d795`.
- All parts except Volume 2, Part IV retain their v1.1.0 teaching baseline. Volume 2, Part IV (Chapters 18–22) covers the preview, with cross-references in the existing chapters and preview sections in the appendices.
- The rescan compared the documentation trees at the stable and preview tags, including published pages, specifications, tutorials, overview material, and proposals. Internal release-checklist changes, dependency lockfiles, navigation wiring, and blog posts are not treated as new teaching chapters.
- `sources-2.0.txt` inventories 41 new or changed teaching sources. `coverage-2.0.csv` maps them to Volume 2, Part IV, with a second reference for the host matrix in Appendix H. Together the maps contain 217 citation assignments; this is not a count of 217 distinct documents.
- Coverage includes all seven client projections, host capabilities, state MCP boundaries, experimental backend/harness contracts, runtime upstream inheritance, upgrade safety, removed personal/consult/global workflows, and proposal status.
- `source-modules.csv` now maps 44 SDK/CLI source modules and files.
- The live documentation can advance beyond this tag. Unreleased changes on `dev` are not asserted to be available in preview.2.

## Automated and integration checks

- `make coverage` checks inventory completeness, chapter citations, and package-module references.
- `make manuscript` checks each volume's chapter sequence (Volume 1: 1–21; Volume 2: 1–25) and matching per-volume solution files, the prerequisites callout, required sections (Configuration Reference and Under the Hood are optional in Volume 1, Chapters 1–4), exercise/quiz solutions, at least two diagrams per chapter, shared appendices A–D and F, Volume 2 appendices G–J, per-volume front matter, and invalid XML control characters.
- `make check` builds both volumes and validates each EPUB using epubcheck. Mermaid rendering is mandatory: a rendering error stops the build rather than leaving diagram source in a published book.
- The Tasktrack API is exercised with `node --test sample/api/test/`. Tests cover health, task creation/listing, invalid and oversized JSON, status changes, missing IDs, and deletion.
- The installed CLI reports `1.1.0`; its help output was checked against the baseline. Writers were instructed to inspect the assigned documentation and implementation and verify commands in disposable repositories.
- An integration audit of explicitly backticked source paths found one nonexistent path, which Volume 2, Chapter 7 (Containers, Cloud Hosting, and Deployment Modes) identifies as an upstream documentation mismatch (`templates/keda/scaler-deployment.yaml` versus the checked-in `templates/keda-scaler.md`).
- HTTP checks of 145 official documentation URLs found two removed live-site pages: consult mode and personal squad. Their manuscript links now point to the corresponding tagged v1.1.0 source files.

## Deliberate limits

This is a complete **first manuscript**, not an independently reviewed publication. Source citations and structural checks do not prove that every explanation or API example is correct. The full prose has not received a separate line-by-line editorial review.

Cloud resources were not provisioned, chargeable services were not invoked, and GitHub Actions was not executed remotely. Infrastructure walkthroughs are source-based teaching material, not proof of a successful Azure deployment. SDK examples were not all compiled or executed. The Tasktrack tests run locally; npm itself was killed by the host environment, so direct Node commands were used for that verification.

The local book build uses Pandoc 3.12.1, epubcheck 5.4.0, Mermaid CLI 12.0.0, and system Chrome. CI is configured separately and should be exercised after the repository is published.

## Updated artifact checks — October 27, 2026

`make check` passed with 217/217 citation assignments, 44/44 source-module references, 47 chapters, zero structural errors, and zero EPUBCheck errors or warnings. `make html` rebuilt the HTML edition. All six Tasktrack API tests passed using the direct Node command above.

The seven external hosts were not each installed, authenticated, and exercised end-to-end. Multi-client commands and examples are source-based preview documentation, not a claim of independent certification of every host integration.

## Two-volume restructure — October 28, 2026

After a structural editorial review, the book was reorganized into two volumes with continuous chapter numbering. Volume 1, *Using Squad*, contains Parts I–IV and Chapters 1–21. Volume 2, *Operating and Extending Squad*, contains Parts V–IX and Chapters 22–46. The old Chapters 2 and 3 were merged. The old client-compatibility chapter was split: dual-mode deployment moved to Chapter 28 and platform adapters moved to Chapter 8. The internals chapters now open Part VII, and the Squad 2.0 preview part comes before Mastery. Each chapter now has a prerequisites line, and the TOC depth was reduced to one level.

`make check` passed with 217/217 citation assignments, 44/44 source-module references, 46 chapters, zero structural errors, and zero EPUBCheck errors or warnings for both `dist/mastering-squad-vol1.epub` and `dist/mastering-squad-vol2.epub`. `make html` rebuilt both HTML editions. All six Tasktrack API tests passed.

## Per-volume chapter numbering

Volume 2 was renumbered to start at Chapter 1: Volume 1 has Chapters 1–21 and Volume 2 has Chapters 1–25 (formerly 22–46).
- Volume 2 chapter files, exercise solutions (now in `exercises/solutions/vol1/` and `exercises/solutions/vol2/`), the chapter manifest, the coverage maps, the source-module map and the Tasktrack tags (`v2-chNN-*`) were updated to match.
- Cross-references within a volume are unqualified. References to the other volume, and all references in the shared appendices, name the volume.
- `make check` passed:
  - 217/217 citations and 44/44 source modules
  - 46 chapters (21 + 25) with zero structural errors
  - Appendix E with 21 and 25 chapter sections
  - zero EPUBCheck errors or warnings for both EPUBs
- `make html` built both volumes, and the sample API tests passed (6/6).

## Per-volume part numbering

Volume 2's parts were renumbered from V–IX to I–V, and their directories were renamed from `book/vol2/part-05…09` to `part-01…05`. References that cross volumes name the volume, for example "Volume 2, Part IV". `make check` and `make html` passed: 217/217 citations, 44/44 modules, 0 structural errors, and 0 EPUBCheck errors or warnings for both EPUBs.
