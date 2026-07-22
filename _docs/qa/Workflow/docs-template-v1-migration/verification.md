---
title: "QA Verification: Docs Template v1 Migration"
status: active
draft_status: n/a
qa_status: verified
risk: Medium
qa_schema: 2
created_at: 2026-07-22
updated_at: 2026-07-22
references:
  - "_docs/intent/Workflow/docs-template-v1-migration/decision.md"
  - "_docs/plan/Workflow/docs-template-v1-migration/plan.md"
  - "_docs/qa/Workflow/docs-template-v1-migration/test-plan.md"
  - "_docs/reference/Workflow/docs-template-v1-migration.md"
related_issues: []
related_prs: []
---

# QA Verification: Docs Template v1 Migration

## Summary

The compatibility migration from legacy baseline
`7ee31b09e355a80b0a3595bea0182b3d5a707ca6` to tag `v1.0.0` at
`f71e9ab20466ea2972158334261f5ae2b2265754` satisfies all in-scope
acceptance criteria. Application behavior and project feature records remain
unchanged. Strict conversion of legacy TODO records is explicitly deferred.

## Verification Verdict

Verdict: PASS

### Compatibility migration

Verdict: PASS

### Strict legacy schema migration

Verdict: PARTIAL

The v1 tooling and all newly created migration records use the current schema.
Existing bullet-form TODO records remain semantically unchanged and are not
rewritten into heading-form records with Risk, AC, Intent, QA, and Verification
fields. The compatibility validator therefore does not provide strict field
coverage for those legacy entries.

## Baseline Results

| Command / Test | Result | Notes |
| --- | --- | --- |
| legacy `validate-frontmatter.mjs` | FAIL | `documentation_guide.md` without frontmatter raised `Unsupported front matter format` |
| legacy Markdown lint scope | FAIL | 144 pre-existing issues in 9 files |
| `uv run pytest` | PASS | 14 tests passed; one dependency deprecation warning |
| `uv build` | PASS | sdist and wheel built |

## Commands Run

```bash
DD_SCOPE_BASE=89c163bb68c5f7b0a561d0849bd52b90cb0c0703 \
  DD_SCOPE_DIFF_FILTER=ACMR ./scripts/check-docs.sh
./scripts/check-docs.sh
npx --yes markdownlint-cli2 '**/*.md' '!.venv/**' '!dist/**' \
  --config .markdownlint.jsonc
deno fmt --check scripts/*.mjs
deno run --allow-read --allow-write --allow-env --allow-run \
  scripts/test-validators.mjs
deno run --allow-read --allow-run=git scripts/test-agent-workflow-hook.mjs
deno run --allow-read scripts/test-agent-workflow-smoke.mjs
diff -rq .agents/skills .claude/skills
uv run python -m compileall -q src tests
uv run pytest
uv build
git -C /home/penne/dev/tools/templates/docs_driven_dev_template \
  rev-parse refs/tags/v1.0.0^{}
git diff --exit-code 89c163bb68c5f7b0a561d0849bd52b90cb0c0703 \
  -- src tests supabase pyproject.toml uv.lock
git diff --exit-code 89c163bb68c5f7b0a561d0849bd52b90cb0c0703 \
  -- _docs/guide/Core _docs/reference/Core _docs/plan/Core
```

Result: all final commands above passed. The resolved tag SHA was
`f71e9ab20466ea2972158334261f5ae2b2265754`.

## Automated Test Results

| Command / Test | Result | Notes |
| --- | --- | --- |
| scoped docs wrapper with `ACMR` | PASS | migrated and edited docs validated |
| unscoped docs wrapper | PASS | existing project docs remain compatible |
| validator fixtures | PASS | valid/invalid TODO, intent, QA, scope, marker type, unknown warning, and duplicate-block cases |
| hook unit and smoke suites | PASS | lifecycle events, guardrails, reader docs, and paired skills |
| full Markdown lint | PASS | 86 Markdown files, zero issues |
| project syntax check | PASS | `src` and `tests` compiled |
| project tests | PASS | 14 passed; one external `audioop` deprecation warning |
| package build | PASS | sdist and wheel produced |

## Manual QA Results

| Checklist Item | Result | Notes |
| --- | --- | --- |
| Three-way inventory coverage | PASS | 138 frozen rows plus migration-created manifest; final raw changed paths had zero missing or unclassified paths |
| Frontmatter uniqueness | PASS | Documentation Guide has one reconciled U metadata block; fixture and focused scan reject consecutive YAML blocks |
| Template-self history exclusion | PASS | no `lifecycle-self-audit` file present |
| Conditional removals | PASS | seven paths met B=P, no-ref, clean-cutoff, and U-absence/replacement gates |
| Project content preservation | PASS | runtime, tests, database, build metadata, and feature docs equal P |
| Branch isolation | PASS | only isolated branch/worktree changed; no push or main update |
| Conflict scan | PASS | no conflict markers found |

## Acceptance Criteria Coverage

| ID | Result | Evidence |
| --- | --- | --- |
| AC-001 | PASS | exact B/P/U in inventory; tag resolves to the supplied full SHA; lock payload reserved for final write |
| AC-002 | PASS | every frozen union path and migration-created artifact is classified |
| AC-003 | PASS | reusable files present; four template-self records absent |
| AC-004 | PASS | scoped/unscoped docs, lint, hook, smoke, fixture, paired, and diff checks passed |
| AC-005 | PASS | deterministic fixture covers valid markers, invalid type, unknown warning, and consecutive duplicate YAML blocks |
| AC-006 | PASS | compatibility PASS and strict schema PARTIAL are separate |
| AC-007 | PASS | removal gate evidence recorded in inventory and manual QA |
| AC-008 | PASS | tests/build passed and application paths have no diff |

## Decision Conformance

| ID | Result | Why the implementation remains aligned |
| --- | --- | --- |
| DEC-001 | PASS | only exact B..U was used; lock was withheld through compatibility QA |
| DEC-002 | PASS | schema-v2 migration records coexist with untouched legacy project records |
| DEC-003 | PASS | project-sensitive files were kept or merged; reusable uncustomized files applied |
| DEC-004 | PASS | template-self history excluded and every removal passed all gates |
| DEC-005 | PASS | frontmatter now validates typed known markers and warns on unknown metadata |

## Review Correction Evidence

- **Root cause**: the frontmatter parser accepted the first closing delimiter
  and did not inspect the next nonblank content, so a second adjacent YAML
  block was treated as document body.
- **Disconfirming check**: the final Documentation Guide begins with exactly
  one block that byte-matches the intended upstream metadata, including the
  security standard reference; the focused scan finds no consecutive duplicate
  YAML blocks under `_docs`.
- **Compatibility boundary**: the detector requires a second delimiter and at
  least one YAML key before its closing delimiter, so a document body that
  intentionally begins with a Markdown horizontal rule remains valid.
- **Inventory correction**: `.codex` is an untracked empty P placeholder and
  has no standalone B/U tree path; its upstream delta is therefore
  `unchanged (absent)`. `.codex/hooks.json` remains the explicit transform.
- **Sentinel correction**: `_docs/qa/.gitkeep` is byte-identical to U's
  one-newline sentinel.

## Invariant Coverage

None

## Deferred / Not Covered

| ID | Reason | Follow-up |
| --- | --- | --- |
| Strict legacy TODO schema | Bulk semantic conversion is outside this migration and could alter active task meaning | Open a separately approved Size M migration before relying on strict field validation for legacy TODO entries |

## Residual Risks

None

## Follow-up TODOs

- Create an owner-approved task to migrate each legacy TODO record
  semantically; do not perform a bulk mechanical rewrite.
