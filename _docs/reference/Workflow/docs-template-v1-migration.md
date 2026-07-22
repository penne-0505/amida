---
title: Docs Template v1 Migration Inventory
status: active
draft_status: n/a
created_at: 2026-07-22
updated_at: 2026-07-22
references:
  - "_docs/plan/Workflow/docs-template-v1-migration/plan.md"
  - "_docs/intent/Workflow/docs-template-v1-migration/decision.md"
  - "_docs/qa/Workflow/docs-template-v1-migration/test-plan.md"
related_issues: []
related_prs: []
---

# Docs Template v1 Migration Inventory

## Provenance and cutoff

- Project repository: `/home/penne/dev/active/amida`
- Isolated worktree: `/tmp/docs-template-v1-rollout/amida`
- Cutoff time: `2026-07-22T12:26:29+09:00`
- `P`: `89c163bb68c5f7b0a561d0849bd52b90cb0c0703`
- `P` state: clean commit, equal to `origin/main`; no staged, unstaged, or
  untracked cutoff paths
- `B`: `7ee31b09e355a80b0a3595bea0182b3d5a707ca6`
- `U`: tag `v1.0.0`,
  `f71e9ab20466ea2972158334261f5ae2b2265754`
- Destination branch: `codex/docs-template-v1-migration`
- Ownership: this worktree only; active checkout, other repositories, remote
  refs, and `main` are outside scope
- Included upstream lane: exactly `B..U`
- Excluded lanes: moving branch tips and every unmerged upstream branch

## Classification rule

The table is the union of the upstream delta `B -> U` and the project delta
`B -> P`. Upstream state and project relation are independent. Every row has
one of the required resolutions: apply, merge, keep, remove, or defer.

## Three-way inventory

| Path | Upstream B to U | Project relation at P | Resolution | Rationale |
| --- | --- | --- | --- | --- |
| `.agents/skills/docs-cleanup/SKILL.md` | added | upstream-owned unmodified (new) | apply | reusable v1 distribution file with no P customization |
| `.agents/skills/docs-inventory/SKILL.md` | added | upstream-owned unmodified (new) | apply | reusable v1 distribution file with no P customization |
| `.agents/skills/docs-prep/SKILL.md` | added | upstream-owned unmodified (new) | apply | reusable v1 distribution file with no P customization |
| `.agents/skills/docs-template-migration/SKILL.md` | added | upstream-owned unmodified (new) | apply | reusable v1 distribution file with no P customization |
| `.agents/skills/implementation-prep/SKILL.md` | added | upstream-owned unmodified (new) | apply | reusable v1 distribution file with no P customization |
| `.agents/skills/post-implementation/SKILL.md` | added | upstream-owned unmodified (new) | apply | reusable v1 distribution file with no P customization |
| `.agents/skills/qa-prep/SKILL.md` | added | upstream-owned unmodified (new) | apply | reusable v1 distribution file with no P customization |
| `.agents/skills/qa-review/SKILL.md` | added | upstream-owned unmodified (new) | apply | reusable v1 distribution file with no P customization |
| `.agents/skills/test-maintenance/SKILL.md` | added | upstream-owned unmodified (new) | apply | reusable v1 distribution file with no P customization |
| `.claude/settings.json` | added | upstream-owned unmodified (new) | apply | reusable v1 distribution file with no P customization |
| `.claude/skills/docs-cleanup/SKILL.md` | added | upstream-owned unmodified (new) | apply | reusable v1 distribution file with no P customization |
| `.claude/skills/docs-inventory/SKILL.md` | added | upstream-owned unmodified (new) | apply | reusable v1 distribution file with no P customization |
| `.claude/skills/docs-prep/SKILL.md` | added | upstream-owned unmodified (new) | apply | reusable v1 distribution file with no P customization |
| `.claude/skills/docs-template-migration/SKILL.md` | added | upstream-owned unmodified (new) | apply | reusable v1 distribution file with no P customization |
| `.claude/skills/implementation-prep/SKILL.md` | added | upstream-owned unmodified (new) | apply | reusable v1 distribution file with no P customization |
| `.claude/skills/post-implementation/SKILL.md` | added | upstream-owned unmodified (new) | apply | reusable v1 distribution file with no P customization |
| `.claude/skills/qa-prep/SKILL.md` | added | upstream-owned unmodified (new) | apply | reusable v1 distribution file with no P customization |
| `.claude/skills/qa-review/SKILL.md` | added | upstream-owned unmodified (new) | apply | reusable v1 distribution file with no P customization |
| `.claude/skills/test-maintenance/SKILL.md` | added | upstream-owned unmodified (new) | apply | reusable v1 distribution file with no P customization |
| `.codex` | unchanged (absent) | project-only | merge | untracked empty P placeholder becomes a hook directory; no guidance content to lose |
| `.codex/hooks.json` | added | upstream-owned unmodified (new) | apply | reusable v1 distribution file with no P customization |
| `.env.example` | unchanged (absent) | project-only | keep | project-only runtime, tests, assets, or project documentation |
| `.github/workflows/docs-ci.yml` | modified | upstream-owned unmodified | merge | project context or pilot behavior merged with reusable v1 content |
| `.gitignore` | unchanged (absent) | project-only | keep | project-only runtime, tests, assets, or project documentation |
| `.markdownlint.jsonc` | modified | upstream-owned unmodified | apply | reusable v1 distribution file with no P customization |
| `.opencode/skills/debug/SKILL.md` | removed | upstream-owned unmodified | remove | B=P exact, no project refs, clean cutoff, and U absent/replaced |
| `.opencode/skills/docs-cleanup/SKILL.md` | removed | upstream-owned unmodified | remove | B=P exact, no project refs, clean cutoff, and U absent/replaced |
| `.opencode/skills/docs-prep/SKILL.md` | removed | upstream-owned unmodified | remove | B=P exact, no project refs, clean cutoff, and U absent/replaced |
| `.opencode/skills/frontend-design/SKILL.md` | removed | upstream-owned unmodified | remove | B=P exact, no project refs, clean cutoff, and U absent/replaced |
| `.opencode/skills/implementation-prep/SKILL.md` | removed | upstream-owned unmodified | remove | B=P exact, no project refs, clean cutoff, and U absent/replaced |
| `.opencode/skills/post-implementation/SKILL.md` | removed | upstream-owned unmodified | remove | B=P exact, no project refs, clean cutoff, and U absent/replaced |
| `.python-version` | unchanged (absent) | project-only | keep | project-only runtime, tests, assets, or project documentation |
| `AGENTS.md` | modified | upstream-owned unmodified | merge | project context or pilot behavior merged with reusable v1 content |
| `CLAUDE.md` | added | upstream-owned unmodified (new) | apply | reusable v1 distribution file with no P customization |
| `LICENSE.txt` | modified | upstream-owned unmodified | keep | project legal authority is not template lifecycle content |
| `QUICKSTART.md` | added | upstream-owned unmodified (new) | apply | reusable v1 distribution file with no P customization |
| `README.md` | modified | customized shared | merge | project context or pilot behavior merged with reusable v1 content |
| `TODO.md` | modified | customized shared | merge | preserve task semantics, remove the completed migration task, and normalize lint-only whitespace; strict conversion deferred |
| `_docs/documentation_guide.md` | modified | upstream-owned unmodified | merge | project context or pilot behavior merged with reusable v1 content |
| `_docs/guide/Core/amidakuji-mvp.md` | unchanged (absent) | project-only | keep | project-only runtime, tests, assets, or project documentation |
| `_docs/guide/Core/healthcheck.md` | unchanged (absent) | project-only | keep | project-only runtime, tests, assets, or project documentation |
| `_docs/intent/Workflow/lifecycle-self-audit/decision.md` | added | upstream-owned unmodified (new) | defer | template-self lifecycle history; downstream import excluded |
| `_docs/plan/Core/template-edit-delete-management.md` | unchanged (absent) | project-only | keep | project-only runtime, tests, assets, or project documentation |
| `_docs/plan/Workflow/lifecycle-self-audit/plan.md` | added | upstream-owned unmodified (new) | defer | template-self lifecycle history; downstream import excluded |
| `_docs/qa/.gitkeep` | added | upstream-owned unmodified (new) | apply | reusable v1 distribution file with no P customization |
| `_docs/qa/Workflow/lifecycle-self-audit/test-plan.md` | added | upstream-owned unmodified (new) | defer | template-self lifecycle history; downstream import excluded |
| `_docs/qa/Workflow/lifecycle-self-audit/verification.md` | added | upstream-owned unmodified (new) | defer | template-self lifecycle history; downstream import excluded |
| `_docs/reference/Core/amidakuji-mvp.md` | unchanged (absent) | project-only | keep | project-only runtime, tests, assets, or project documentation |
| `_docs/reference/Core/healthcheck.md` | unchanged (absent) | project-only | keep | project-only runtime, tests, assets, or project documentation |
| `_docs/standards/documentation_guidelines.md` | modified | upstream-owned unmodified | apply | reusable v1 distribution file with no P customization |
| `_docs/standards/documentation_operations.md` | modified | upstream-owned unmodified | apply | reusable v1 distribution file with no P customization |
| `_docs/standards/jj_workflow.md` | removed | upstream-owned unmodified | remove | B=P exact, no project refs, clean cutoff, and U absent/replaced |
| `_docs/standards/quality_assurance.md` | added | upstream-owned unmodified (new) | apply | reusable v1 distribution file with no P customization |
| `_docs/standards/security_for_agents.md` | added | upstream-owned unmodified (new) | apply | reusable v1 distribution file with no P customization |
| `_docs/standards/templates/draft.md` | modified | upstream-owned unmodified | apply | reusable v1 distribution file with no P customization |
| `_docs/standards/templates/guide.md` | modified | upstream-owned unmodified | apply | reusable v1 distribution file with no P customization |
| `_docs/standards/templates/intent.md` | modified | upstream-owned unmodified | apply | reusable v1 distribution file with no P customization |
| `_docs/standards/templates/plan.md` | modified | upstream-owned unmodified | apply | reusable v1 distribution file with no P customization |
| `_docs/standards/templates/qa-test-plan.md` | added | upstream-owned unmodified (new) | apply | reusable v1 distribution file with no P customization |
| `_docs/standards/templates/qa-verification.md` | added | upstream-owned unmodified (new) | apply | reusable v1 distribution file with no P customization |
| `_docs/standards/templates/reference.md` | modified | upstream-owned unmodified | apply | reusable v1 distribution file with no P customization |
| `_docs/standards/templates/survey.md` | modified | upstream-owned unmodified | apply | reusable v1 distribution file with no P customization |
| `_evals/agent-workflows/README.md` | added | upstream-owned unmodified (new) | apply | reusable v1 distribution file with no P customization |
| `_evals/agent-workflows/cases/agent-workflow-misbehavior-check.md` | added | upstream-owned unmodified (new) | apply | reusable v1 distribution file with no P customization |
| `_evals/agent-workflows/cases/archive-flow.md` | added | upstream-owned unmodified (new) | apply | reusable v1 distribution file with no P customization |
| `_evals/agent-workflows/cases/blocked-verification.md` | added | upstream-owned unmodified (new) | apply | reusable v1 distribution file with no P customization |
| `_evals/agent-workflows/cases/breaking-change.md` | added | upstream-owned unmodified (new) | apply | reusable v1 distribution file with no P customization |
| `_evals/agent-workflows/cases/bug-regression-test.md` | added | upstream-owned unmodified (new) | apply | reusable v1 distribution file with no P customization |
| `_evals/agent-workflows/cases/experimental-baseline.md` | added | upstream-owned unmodified (new) | apply | reusable v1 distribution file with no P customization |
| `_evals/agent-workflows/cases/high-risk-change-verification.md` | added | upstream-owned unmodified (new) | apply | reusable v1 distribution file with no P customization |
| `_evals/agent-workflows/cases/historical-prompt-not-operational.md` | added | upstream-owned unmodified (new) | apply | reusable v1 distribution file with no P customization |
| `_evals/agent-workflows/cases/intentional-omission-risk.md` | added | upstream-owned unmodified (new) | apply | reusable v1 distribution file with no P customization |
| `_evals/agent-workflows/cases/malformed-todo-heading.md` | added | upstream-owned unmodified (new) | apply | reusable v1 distribution file with no P customization |
| `_evals/agent-workflows/cases/medium-feature.md` | added | upstream-owned unmodified (new) | apply | reusable v1 distribution file with no P customization |
| `_evals/agent-workflows/cases/misleading-optimization.md` | added | upstream-owned unmodified (new) | apply | reusable v1 distribution file with no P customization |
| `_evals/agent-workflows/cases/qa-prep-from-intent.md` | added | upstream-owned unmodified (new) | apply | reusable v1 distribution file with no P customization |
| `_evals/agent-workflows/cases/qa-status-verdict-mismatch.md` | added | upstream-owned unmodified (new) | apply | reusable v1 distribution file with no P customization |
| `_evals/agent-workflows/cases/rationale-preserving-change.md` | added | upstream-owned unmodified (new) | apply | reusable v1 distribution file with no P customization |
| `_evals/agent-workflows/cases/refactor-behavior-preservation.md` | added | upstream-owned unmodified (new) | apply | reusable v1 distribution file with no P customization |
| `_evals/agent-workflows/cases/small-bug.md` | added | upstream-owned unmodified (new) | apply | reusable v1 distribution file with no P customization |
| `_evals/agent-workflows/cases/stale-draft-cleanup.md` | added | upstream-owned unmodified (new) | apply | reusable v1 distribution file with no P customization |
| `_evals/agent-workflows/cases/template-version-migration.md` | added | upstream-owned unmodified (new) | apply | reusable v1 distribution file with no P customization |
| `_evals/agent-workflows/expected-invariants.md` | added | upstream-owned unmodified (new) | apply | reusable v1 distribution file with no P customization |
| `_evals/validator-fixtures/README.md` | added | upstream-owned unmodified (new) | apply | reusable v1 distribution file with no P customization |
| `_evals/validator-fixtures/intent/invalid/missing-why.md` | added | upstream-owned unmodified (new) | apply | reusable v1 distribution file with no P customization |
| `_evals/validator-fixtures/intent/invalid/orphan-invariant.md` | added | upstream-owned unmodified (new) | apply | reusable v1 distribution file with no P customization |
| `_evals/validator-fixtures/intent/valid/decision.md` | added | upstream-owned unmodified (new) | apply | reusable v1 distribution file with no P customization |
| `_evals/validator-fixtures/links/valid-reference-anchor.md` | added | upstream-owned unmodified (new) | apply | reusable v1 distribution file with no P customization |
| `_evals/validator-fixtures/qa/invalid/missing-invariant.md` | added | upstream-owned unmodified (new) | apply | reusable v1 distribution file with no P customization |
| `_evals/validator-fixtures/qa/invalid/qa-archive-path.md` | added | upstream-owned unmodified (new) | apply | reusable v1 distribution file with no P customization |
| `_evals/validator-fixtures/qa/invalid/status-verdict-mismatch.md` | added | upstream-owned unmodified (new) | apply | reusable v1 distribution file with no P customization |
| `_evals/validator-fixtures/qa/invalid/v2-missing-decision-scope.md` | added | upstream-owned unmodified (new) | apply | reusable v1 distribution file with no P customization |
| `_evals/validator-fixtures/qa/invalid/verification-in-progress-status.md` | added | upstream-owned unmodified (new) | apply | reusable v1 distribution file with no P customization |
| `_evals/validator-fixtures/qa/invalid/verification-missing-test-plan-reference.md` | added | upstream-owned unmodified (new) | apply | reusable v1 distribution file with no P customization |
| `_evals/validator-fixtures/qa/valid/test-plan.md` | added | upstream-owned unmodified (new) | apply | reusable v1 distribution file with no P customization |
| `_evals/validator-fixtures/qa/valid/verification-pass.md` | added | upstream-owned unmodified (new) | apply | reusable v1 distribution file with no P customization |
| `_evals/validator-fixtures/todo/invalid/malformed-heading.md` | added | upstream-owned unmodified (new) | apply | reusable v1 distribution file with no P customization |
| `_evals/validator-fixtures/todo/invalid/mismatched-heading-id.md` | added | upstream-owned unmodified (new) | apply | reusable v1 distribution file with no P customization |
| `_evals/validator-fixtures/todo/invalid/missing-qa-for-medium.md` | added | upstream-owned unmodified (new) | apply | reusable v1 distribution file with no P customization |
| `_evals/validator-fixtures/todo/invalid/missing-title.md` | added | upstream-owned unmodified (new) | apply | reusable v1 distribution file with no P customization |
| `_evals/validator-fixtures/todo/valid/basic.md` | added | upstream-owned unmodified (new) | apply | reusable v1 distribution file with no P customization |
| `docs-template.lock.example.json` | added | upstream-owned unmodified (new) | apply | reusable v1 distribution file with no P customization |
| `pyproject.toml` | unchanged (absent) | project-only | keep | project-only runtime, tests, assets, or project documentation |
| `scripts/agent-workflow-hook.mjs` | added | upstream-owned unmodified (new) | apply | reusable v1 distribution file with no P customization |
| `scripts/check-docs.sh` | added | upstream-owned unmodified (new) | apply | reusable v1 distribution file with no P customization |
| `scripts/create-template-archive.sh` | added | upstream-owned unmodified (new) | apply | reusable v1 distribution file with no P customization |
| `scripts/scope.mjs` | added | upstream-owned unmodified (new) | apply | reusable v1 distribution file with no P customization |
| `scripts/test-agent-workflow-hook.mjs` | added | upstream-owned unmodified (new) | merge | project context or pilot behavior merged with reusable v1 content |
| `scripts/test-agent-workflow-smoke.mjs` | added | upstream-owned unmodified (new) | apply | reusable v1 distribution file with no P customization |
| `scripts/test-validators.mjs` | added | upstream-owned unmodified (new) | merge | project context or pilot behavior merged with reusable v1 content |
| `scripts/validate-doc-links.mjs` | added | upstream-owned unmodified (new) | apply | reusable v1 distribution file with no P customization |
| `scripts/validate-frontmatter.mjs` | modified | upstream-owned unmodified | merge | project context or pilot behavior merged with reusable v1 content |
| `scripts/validate-intent.mjs` | added | upstream-owned unmodified (new) | apply | reusable v1 distribution file with no P customization |
| `scripts/validate-qa.mjs` | added | upstream-owned unmodified (new) | apply | reusable v1 distribution file with no P customization |
| `scripts/validate-todo.mjs` | added | upstream-owned unmodified (new) | apply | reusable v1 distribution file with no P customization |
| `src/amida_bot/__init__.py` | unchanged (absent) | project-only | keep | project-only runtime, tests, assets, or project documentation |
| `src/amida_bot/__main__.py` | unchanged (absent) | project-only | keep | project-only runtime, tests, assets, or project documentation |
| `src/amida_bot/application/__init__.py` | unchanged (absent) | project-only | keep | project-only runtime, tests, assets, or project documentation |
| `src/amida_bot/application/amidakuji_service.py` | unchanged (absent) | project-only | keep | project-only runtime, tests, assets, or project documentation |
| `src/amida_bot/config.py` | unchanged (absent) | project-only | keep | project-only runtime, tests, assets, or project documentation |
| `src/amida_bot/discord_ui/__init__.py` | unchanged (absent) | project-only | keep | project-only runtime, tests, assets, or project documentation |
| `src/amida_bot/discord_ui/amidakuji_flow.py` | unchanged (absent) | project-only | keep | project-only runtime, tests, assets, or project documentation |
| `src/amida_bot/discord_ui/bot.py` | unchanged (absent) | project-only | keep | project-only runtime, tests, assets, or project documentation |
| `src/amida_bot/domain/__init__.py` | unchanged (absent) | project-only | keep | project-only runtime, tests, assets, or project documentation |
| `src/amida_bot/domain/models.py` | unchanged (absent) | project-only | keep | project-only runtime, tests, assets, or project documentation |
| `src/amida_bot/domain/raffle.py` | unchanged (absent) | project-only | keep | project-only runtime, tests, assets, or project documentation |
| `src/amida_bot/errors.py` | unchanged (absent) | project-only | keep | project-only runtime, tests, assets, or project documentation |
| `src/amida_bot/healthcheck.py` | unchanged (absent) | project-only | keep | project-only runtime, tests, assets, or project documentation |
| `src/amida_bot/infra/__init__.py` | unchanged (absent) | project-only | keep | project-only runtime, tests, assets, or project documentation |
| `src/amida_bot/infra/supabase_client.py` | unchanged (absent) | project-only | keep | project-only runtime, tests, assets, or project documentation |
| `src/amida_bot/persistence/__init__.py` | unchanged (absent) | project-only | keep | project-only runtime, tests, assets, or project documentation |
| `src/amida_bot/persistence/guild_template_repository.py` | unchanged (absent) | project-only | keep | project-only runtime, tests, assets, or project documentation |
| `src/amida_bot/persistence/last_used_template_repository.py` | unchanged (absent) | project-only | keep | project-only runtime, tests, assets, or project documentation |
| `supabase/migrations/20260410_000001_amida_mvp.sql` | unchanged (absent) | project-only | keep | project-only runtime, tests, assets, or project documentation |
| `tests/test_amidakuji_service.py` | unchanged (absent) | project-only | keep | project-only runtime, tests, assets, or project documentation |
| `tests/test_healthcheck.py` | unchanged (absent) | project-only | keep | project-only runtime, tests, assets, or project documentation |
| `tests/test_raffle.py` | unchanged (absent) | project-only | keep | project-only runtime, tests, assets, or project documentation |
| `uv.lock` | unchanged (absent) | project-only | keep | project-only runtime, tests, assets, or project documentation |

## Migration-created artifact manifest

These paths were absent from the initial union or are explicit path
transformations created by this migration. The final diff reconciliation treats
them as inventory-covered.

| Path | Source | Resolution | Rationale |
| --- | --- | --- | --- |
| `.codex/hooks.json` | U path replacing empty P placeholder | apply | Codex lifecycle hook configuration |
| `docs-template.lock.json` | migration-created | apply | first lock, written only after compatibility PASS |
| `_docs/plan/Workflow/docs-template-v1-migration/plan.md` | migration-created | apply | migration contract |
| `_docs/intent/Workflow/docs-template-v1-migration/decision.md` | migration-created | apply | durable migration decisions |
| `_docs/qa/Workflow/docs-template-v1-migration/test-plan.md` | migration-created | apply | pre-implementation QA matrix |
| `_docs/qa/Workflow/docs-template-v1-migration/verification.md` | migration-created | apply | closure evidence |
| `_docs/reference/Workflow/docs-template-v1-migration.md` | migration-created | apply | inventory and reconciliation |

## Removal authorization evidence

The six `.opencode/skills/**` files and
`_docs/standards/jj_workflow.md` satisfy all deletion gates:

- their blobs at `B` and `P` are byte-identical;
- repository search at `P` finds no project reference to those paths or the
  Jujutsu workflow outside the obsolete file itself;
- no post-cutoff project changes exist in the isolated worktree;
- `U` removes them, while paired `.agents` / `.claude` skills replace the
  reusable workflow coverage.

The files were moved to
`/tmp/docs-template-v1-rollout/amida-obsolete/` during reconciliation rather
than permanently deleted from the host.

The four `lifecycle-self-audit` documents are upstream template-self plan,
intent, QA plan, and verification history. They are excluded rather than
imported and never become Amida project records.

## Preservation boundary

The final reconciliation must show no changes under `src/`, `tests/`,
`supabase/`, `pyproject.toml`, `uv.lock`, `.env.example`,
`.python-version`, or `.gitignore`. Existing project guide, reference, and
feature plan documents remain byte-identical to `P`. README and AGENTS are
merged rather than replaced.
