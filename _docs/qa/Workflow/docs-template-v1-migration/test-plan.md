---
title: "QA Test Plan: Docs Template v1 Migration"
status: active
draft_status: n/a
qa_status: planned
risk: Medium
qa_schema: 2
created_at: 2026-07-22
updated_at: 2026-07-22
references:
  - "_docs/intent/Workflow/docs-template-v1-migration/decision.md"
  - "_docs/plan/Workflow/docs-template-v1-migration/plan.md"
  - "_docs/reference/Workflow/docs-template-v1-migration.md"
related_issues: []
related_prs: []
---

# QA Test Plan: Docs Template v1 Migration

## Source of Intent

- TODO: `Workflow-Chore-5`
- Plan: `_docs/plan/Workflow/docs-template-v1-migration/plan.md`
- Intent: `_docs/intent/Workflow/docs-template-v1-migration/decision.md`

## Quality Goal

Adopt the reusable v1 docs workflow with exact provenance and deterministic
validation while preserving all Amida application behavior and project-owned
records.

## Acceptance Criteria

- AC-001: `B`, `P`, tag `v1.0.0`, and full `U` SHA are recorded and verified.
- AC-002: every path in `B -> U` and `B -> P`, plus every migration-created
  artifact, has one classification and resolution.
- AC-003: reusable standards, templates, paired skills, hooks, validators,
  fixtures, docs CI, and root guidance are reconciled; template-self lifecycle
  records are not imported.
- AC-004: CI uses `DD_SCOPE_BASE=P` and `DD_SCOPE_DIFF_FILTER=ACMR`; scoped and
  appropriate unscoped docs checks, full markdownlint, hooks, smoke, fixtures,
  paired checks, and diff checks pass.
- AC-005: frontmatter accepts supported numeric `intent_schema` and
  `qa_schema`, rejects invalid marker values/types, and warns for an unknown
  field under deterministic tests.
- AC-006: compatibility and strict legacy schema outcomes are reported
  separately, with strict bulk conversion deferred.
- AC-007: removals satisfy exact B=P, no project references, clean cutoff, and
  U absent or replacement evidence.
- AC-008: project pytest and package build pass, and final diff contains no
  source, test, build metadata, database, asset, or runtime configuration
  change.

## Decision Review Scope

- DEC-001: provenance lock timing and exact revisions
- DEC-002: compatibility versus strict schema boundary
- DEC-003: pathwise reconciliation and preservation
- DEC-004: template history exclusion and removal gates
- DEC-005: typed schema marker handling

## Intent-derived Invariants

None

## Risk Assessment

- Risk level: Medium
- Risk rationale: docs CI, validators, hooks, and agent instructions change
  repository-wide development behavior.
- Regression risk: replacing root or standards files could discard project
  instructions or make existing docs fail CI.
- Data safety risk: none; no runtime data path is in scope.
- Security / privacy risk: hooks and CI are reviewed before execution and no
  secret-bearing file is imported.
- UX risk: no user-facing application behavior change.
- Agent misbehavior risk: branch mixing, blind replacement, premature lock
  write, unjustified deletion, and bulk schema conversion.

## Test Strategy

- Unit: upstream validator fixture runner and hook unit tests.
- Integration: unscoped and scoped docs wrappers plus docs CI configuration.
- E2E: hook smoke runner and package build.
- Manual QA: inventory, provenance, deletion gates, and preservation diff.
- Validator / static check: Deno format, all validators, full markdownlint,
  paired-skill byte comparison, conflict-marker scan.
- Diff review: compare `P..HEAD` names and blobs against the inventory and
  migration-created manifest.

## Test Matrix

| ID | Source | Requirement / Optional Invariant | Test Type | Command / File | Expected Evidence | Status |
| --- | --- | --- | --- | --- | --- | --- |
| AC-001 | TODO | Exact provenance | static | `git -C <upstream> rev-parse refs/tags/v1.0.0^{}` | Full SHA matches lock | verified |
| AC-002 | TODO | Inventory covers final diff | diff | inventory reconciliation script | No unclassified path | verified |
| AC-003 | TODO | Reusable files and exclusions | diff | upstream/project path comparison | Intended apply/defer states | verified |
| AC-004 | TODO | Docs and workflow checks | integration | `./scripts/check-docs.sh` and targeted runners | All selected checks pass | verified |
| AC-005 | DEC-005 | Schema marker handling | validator | `scripts/test-validators.mjs` | Known valid, invalid, and unknown cases pass | verified |
| AC-006 | DEC-002 | Separate verdicts | review | migration verification | Compatibility and strict outcomes differ explicitly | verified |
| AC-007 | DEC-004 | Deletion gates | static | blob and `rg` checks | Every removed path meets all gates | verified |
| AC-008 | TODO | Application preservation | regression | `uv run pytest && uv build` plus diff | Tests/build pass; app paths unchanged | verified |

## Manual QA Checklist

- [x] Confirm active checkout and other repositories remain untouched.
- [x] Confirm no template-self lifecycle document is present.
- [x] Confirm README project setup and runtime details remain present.
- [x] Confirm TODO project task state remains present and unconverted.
- [x] Confirm lock is reserved as the final migration write before closure reruns.

## Regression Checklist

- [x] No `src/`, `tests/`, `supabase/`, dependency lock, or build metadata diff.
- [x] Existing project guide, reference, and feature plan blobs equal `P`.
- [x] `.agents` and `.claude` paired skills are byte-identical.
- [x] Hook configurations reference the imported common script.
- [x] No conflict markers or untracked build artifacts enter the commit.

## Agent Misbehavior Checks

- [x] Reject moving branch tips or a range other than exact `B..U`.
- [x] Detect replacement of customized README or TODO content.
- [x] Detect a lock created before compatibility checks.
- [x] Detect removal lacking one of the four deletion gates.
- [x] Detect bulk schema edits to legacy project records.

## Out of Scope

- Runtime and feature behavior, strict conversion of all legacy project docs,
  remote operations, and upstream template modifications.

## Open Questions

- None. The owner supplied the exact revisions, isolated destination, required
  pilot behavior, and deletion conditions.
