---
title: Docs Template v1 Migration Plan
status: active
draft_status: n/a
created_at: 2026-07-22
updated_at: 2026-07-22
references:
  - "_docs/intent/Workflow/docs-template-v1-migration/decision.md"
  - "_docs/qa/Workflow/docs-template-v1-migration/test-plan.md"
  - "_docs/reference/Workflow/docs-template-v1-migration.md"
related_issues: []
related_prs: []
---

# Docs Template v1 Migration Plan

## Overview

Migrate the legacy docs-driven template baseline in Amida to the pinned
`v1.0.0` release without changing application behavior or replacing project
customizations. This is a legacy bootstrap: the project has no provenance lock,
but the owner supplied an exact prior baseline `B` and cutoff `P`.

## Evidence and competing explanation

The migration need is evidenced by the absence of `docs-template.lock.json`,
paired agent skills, QA validators, hooks, and the v1 standards at `P`. The
supplied `B` is corroborated because every path from the 32-file `B` tree is
present at `P`; 30 blobs are byte-identical and the two differing files are the
expected project-customized `README.md` and `TODO.md`.

A plausible disconfirming explanation is that the project was based on a
different unrecorded template revision whose files happened to overlap with
`B`. The exact full SHA supplied by the owner, complete path coverage, and
matching blobs make that explanation inconsistent with the available evidence.
No moving branch or inferred replacement baseline is used.

## Scope

- Reconcile the exact upstream range `B..U` recorded in the inventory.
- Import reusable standards, templates, paired skills, hooks, validators,
  fixtures, docs CI, and shared root guidance path by path.
- Preserve project source, tests, database migration, build metadata, runtime
  configuration examples, project README content, TODO state, and feature docs.
- Add a first provenance lock only after compatibility checks pass.
- Record compatibility and strict schema outcomes separately.
- Commit one coherent migration commit on the isolated branch.

## Non-Goals

- No application feature, dependency, data model, or runtime behavior change.
- No bulk conversion of legacy TODO entries or project feature documents.
- No import of upstream template-self lifecycle plan, intent, or QA history.
- No push, pull request, remote ref update, or update to `main`.
- No cleanup outside the exact removal gates in the inventory.

## Requirements

- **Functional**: v1 docs tooling must run from this repository, CI must use
  `DD_SCOPE_BASE=P` and `DD_SCOPE_DIFF_FILTER=ACMR`, and the lock must name tag
  `v1.0.0` with its exact full SHA.
- **Compatibility**: unchanged legacy project docs and TODO records remain
  intact. New migration docs use schema v2 and are validated in scope.
- **Validation**: frontmatter recognizes numeric `intent_schema` and
  `qa_schema` as known fields while preserving warnings for genuinely unknown
  fields; deterministic tests cover both paths.
- **Preservation**: final diff contains no application/runtime/test/build/data
  path unless it is listed as a migration artifact.
- **Operations**: provenance resolution commands use `git -C` against the
  upstream template checkout.

## Non-local effects reviewed

- **Callers and data flow**: no Python module, Discord command, Supabase query,
  environment variable, or runtime entry point changes.
- **Tests and CI**: docs CI expands from two checks to the v1 wrapper and uses a
  full history checkout for scoped validation. Project pytest and package build
  remain independent closure gates.
- **Docs**: standards and authoring templates change for future work. Existing
  project feature docs remain legacy-compatible until semantically edited.
- **Operations**: lifecycle hooks add review prompts and deletion guards but do
  not mutate docs or runtime state.
- **Maintenance**: future template upgrades use the lock and three-way
  migration skill; strict TODO conversion remains an explicit follow-up rather
  than hidden compatibility debt.

## Tasks

1. Freeze and record `P`, `B`, `U`, baseline failures, and the full inventory.
2. Create Plan, Intent, and QA test-plan before importing implementation files.
3. Import reusable v1 files and remove only paths satisfying every deletion
   gate.
4. Merge project-sensitive root guidance, CI, and frontmatter behavior.
5. Run compatibility, fixture, hook, paired-skill, markdown, project test, and
   build checks.
6. Write verification, run QA review, reconcile the final diff to inventory,
   and only then create the lock.
7. Commit without pushing or updating `main`.

## QA Plan

The canonical test matrix is in
`_docs/qa/Workflow/docs-template-v1-migration/test-plan.md`. It includes agent
misbehavior checks for branch mixing, blind replacement, premature lock
advancement, unsupported deletion, and bulk schema conversion.

## Deployment / Rollout

The output is a local branch and commit only. Adoption into `main` is outside
this task. Rollback is the omission of that commit; no runtime or data rollback
is needed.
