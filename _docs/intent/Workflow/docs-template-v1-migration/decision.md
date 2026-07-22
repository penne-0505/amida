---
title: Docs Template v1 Migration Decisions
status: active
draft_status: n/a
intent_schema: 2
created_at: 2026-07-22
updated_at: 2026-07-22
references:
  - "_docs/plan/Workflow/docs-template-v1-migration/plan.md"
  - "_docs/qa/Workflow/docs-template-v1-migration/test-plan.md"
  - "_docs/reference/Workflow/docs-template-v1-migration.md"
related_issues: []
related_prs: []
---

# Docs Template v1 Migration Decisions

## Context

Amida adopted a pre-v1 docs-driven template and customized its project README
and task state without recording template provenance. The repository now needs
the reusable v1 workflow while retaining application behavior and project
records.

## Decisions

### DEC-001: Pin the legacy bootstrap and release provenance

- **What**: Use the owner-confirmed `B`, clean project cutoff `P`, and tag plus
  full SHA for `U`; create the first lock only after compatibility succeeds.
- **Why**: A moving branch or inferred baseline could mix unrelated upstream
  changes and make later migrations irreproducible.
- **Why not**: `DD_SCOPE_BASE` is not provenance; it only selects project-local
  validator scope.
- **Change freedom**: The inventory format and verification commands may
  change if they continue to prove the same three exact revisions and timing.
- **Revisit when**: Upstream publishes a signed provenance format that retains
  the same or stronger reproducibility.

### DEC-002: Separate compatibility from strict schema adoption

- **What**: Import v1 validators in legacy-compatible operation, validate new
  migration docs with schema v2, and defer bulk TODO and feature-doc conversion.
- **Why**: Template tooling can become current without rewriting project task
  meaning or manufacturing decisions for historical documents.
- **Why not**: Bulk schema conversion would obscure semantic changes inside a
  mechanical migration and could alter the active task contract.
- **Change freedom**: Legacy records may be migrated individually when their
  meaning changes; the follow-up may use any safe ordering.
- **Revisit when**: A dedicated owner-approved task defines how each legacy
  TODO record maps to Risk, AC, Intent, QA, and Verification.

### DEC-003: Reconcile project-sensitive files path by path

- **What**: Keep project README, TODO, and license authority; merge AGENTS, CI,
  `.codex`, and frontmatter behavior; apply uncustomized reusable files.
- **Why**: Whole-tree replacement would overwrite Amida-specific runtime docs
  and task state even though most reusable template paths are safe to import.
- **Why not**: Blob equality alone does not authorize replacing legal or
  project-state files whose authority belongs to the downstream repository.
- **Change freedom**: Reusable files may later diverge locally when a project
  requirement is documented and the next migration inventory records it.

### DEC-004: Exclude template history and gate every removal

- **What**: Do not import the four `lifecycle-self-audit` records. Remove the
  six obsolete `.opencode` skills and `jj_workflow.md` only after exact B=P
  equality, no-reference search, clean cutoff, and U removal are all proven.
- **Why**: Upstream lifecycle evidence is not project history, while unproven
  deletion could destroy downstream guidance.
- **Change freedom**: Additional template-self records may be excluded when
  classified explicitly; project records require separate owner authority.

### DEC-005: Treat schema markers as typed known frontmatter

- **What**: The frontmatter validator recognizes `intent_schema` and
  `qa_schema`, accepts the supported numeric value, rejects wrong types or
  unsupported values, and still warns for unknown fields.
- **Why**: The intent and QA validators depend on these markers; frontmatter
  must not describe valid v1 documents as containing unknown metadata.
- **Change freedom**: Supported schema values and parser organization may
  evolve together with the specialized validators and fixtures.

## Consequences / Impact

- The docs workflow and agent guardrails become v1-current.
- Existing project task and feature documentation remain semantically stable.
- CI covers edited docs using `ACMR`, but strict conversion of legacy TODO
  records remains deferred and visible in verification.
- No application runtime, persistence, build, or dependency path changes.

## Quality Implications

- Provenance, inventory coverage, and preservation require diff-based evidence.
- Validator fixtures must distinguish recognized schema markers from unknown
  metadata.
- Compatibility can receive PASS while strict schema adoption receives
  PARTIAL; those verdicts must not be collapsed.

## Intent-derived Invariants

None

## Enforced in (optional)

- DEC-001: `docs-template.lock.json`, migration inventory, verification
- DEC-002: scoped CI, migration verification
- DEC-003: final diff and preservation checks
- DEC-004: inventory classification and no-reference search
- DEC-005: `scripts/validate-frontmatter.mjs` and validator fixture runner

## Rollback / Follow-ups

- Rollback is to omit the migration commit from project history.
- Follow up with a separately approved strict migration of legacy TODO records.
