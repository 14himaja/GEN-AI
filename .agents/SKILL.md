---
name: synxa-master-skill
version: "1.0.0"
description: >
  Master orchestration skill for SYNXA-LEARN workspace. Activate for EVERY task:
  bug fixes, new features, upgrades, architecture changes, UI work, or documentation.
  This skill reads all 9 sub-skills and enforces a structured, senior-developer
  quality implementation flow across every project in this workspace.
triggers:
  - "bug"
  - "fix"
  - "feature"
  - "implement"
  - "build"
  - "create"
  - "upgrade"
  - "refactor"
  - "review"
  - "design"
  - "deploy"
  - "test"
  - "debug"
  - "error"
  - "issue"
  - "improve"
  - "add"
  - "update"
  - "change"
  - "integrate"
always_active: true
---

# SYNXA Master Skill — Structured Development Flow

> **This skill is ALWAYS active.** Every request, no matter how small, runs through
> this structured flow. The sub-skills below are loaded on-demand based on the task type.

---

## 🧠 PHASE 0 — UNDERSTAND BEFORE TOUCHING CODE

> Skill sources: **ponytail** (lazy senior dev) + **karpathy-skills** (think before coding)

**STOP. Read. Trace. Then act.**

Before writing a single line of code:

1. **Read the full request** — identify WHAT is asked, not what you assume.
2. **Surface assumptions explicitly** — if multiple interpretations exist, list them and ask.
3. **Trace the real flow end-to-end** — read the code it touches, find all callers.
4. **Apply the YAGNI ladder:**
   - Does this need to be built at all?
   - Does it already exist in this codebase? Reuse it.
   - Does the standard library / installed dep already do this? Use it.
   - Can this be one line? Make it one line.
   - Only then: write the minimum code that works.
5. **Bug = root cause, not symptom** — grep every caller, fix the shared function once.

```
ponytail:comment format → ponytail: <ceiling description> / upgrade path: <what to do later>
```

---

## 📋 PHASE 1 — PLAN (For Complex Tasks)

> Skill sources: **ECC** (planner agent) + **gstack** (/autoplan + /spec) + **ruflo** (coordination)

**Use this phase for:** new features, architectural changes, multi-file refactors.
**Skip this phase for:** trivial one-liners, simple bug fixes, formatting.

### 1.1 Select the Right Agents

| Task Type | Invoke |
|-----------|--------|
| Complex feature / multi-file change | `planner` agent (ECC) |
| Architectural decision | `architect` agent (ECC) |
| Bug fix | `investigate` skill (gstack) |
| New project planning | `/autoplan` → CEO → design → DX → eng review |
| Vague request → precise spec | `/spec` (gstack) |
| Security-sensitive code | `security-reviewer` (ECC) |
| RAG / ML pipeline | `rag-pipeline-reviewer` or `mle-reviewer` (ECC) |

### 1.2 Plan Format

For multi-step tasks, always state a brief plan:
```
1. [Step] → verify: [check]
2. [Step] → verify: [check]
3. [Step] → verify: [check]
```

### 1.3 Design Review (if UI involved)

Run `/plan-design-review` (gstack) — rate each design dimension 0-10.
Consult ui-ux-pro-max search before writing any CSS/styles:
```bash
python3 .agents/skills/ui-ux-pro-max/src/ui-ux-pro-max/scripts/search.py "<query>" --domain style
```

---

## 🏗️ PHASE 2 — ARCHITECTURE & DESIGN

> Skill sources: **open-design** (design systems) + **ui-ux-pro-max** (design intelligence) + **superpowers** (PR hygiene) + **gstack** (/design-consultation)

### 2.1 Architecture Principles

- **Clean, layered architecture** — separate concerns: presentation / business logic / data
- **No abstractions unless requested** — YAGNI
- **Immutability first** — create new objects, never mutate
- **Security-first by design** — validate all inputs at trust boundaries
- **One source of truth** — no duplicated logic across files

### 2.2 UI/Design Standards

Before implementing any UI component:
1. Search for typography: `python3 ... search.py "saas dashboard" --domain typography`
2. Search for color palette: `python3 ... search.py "dark mode" --domain color`
3. Search for UX patterns: `python3 ... search.py "form validation" --domain ux`
4. Check style: `python3 ... search.py "glassmorphism" --domain style`
5. For animations: `python3 ... search.py "hover" --domain gsap`

### 2.3 File Structure Conventions

```
project/
├── src/              # All source code (clean, no mixed concerns)
├── tests/            # Test files mirror src/ structure
├── docs/             # Documentation (auto-generated via gstack /document-generate)
├── .env.example      # Never commit .env, always provide example
└── README.md         # Always up-to-date
```

---

## ✍️ PHASE 3 — IMPLEMENTATION

> Skill sources: **ponytail** (efficient code) + **karpathy-skills** (surgical changes) + **ECC** (TDD + security) + **ruflo** (concurrent execution)

### 3.1 Code Quality Rules

- **Simplicity first** — if you write 200 lines and it could be 50, rewrite it.
- **Surgical changes** — touch ONLY what you must. Match existing style.
- **Test-driven** — write tests before implementation (or at minimum alongside).
- **No boilerplate nobody asked for** — no extra abstractions, no over-engineering.
- **Boring over clever** — the least surprising solution wins.
- **Document your intent** — preserve all existing comments; add new ones where non-obvious.

### 3.2 Security Checklist (ALWAYS before commit)

```
☐ No hardcoded secrets (API keys, passwords, tokens)
☐ All user inputs validated at trust boundaries
☐ SQL injection prevention (parameterized queries)
☐ XSS prevention (sanitized HTML output)
☐ CSRF protection enabled
☐ Authentication/authorization verified
☐ Rate limiting on all API endpoints
☐ Error messages do NOT leak sensitive data
☐ .env excluded from git, .env.example provided
```

### 3.3 Language-Specific Reviewers (ECC agents)

| Language | Use Agent |
|----------|-----------|
| Python | `python-reviewer` |
| TypeScript/JS | `typescript-reviewer` |
| Go | `go-reviewer` |
| Rust | `rust-reviewer` |
| Java/Spring | `java-reviewer` |
| Django | `django-reviewer` |
| Database/SQL | `database-reviewer` |
| ML/AI pipelines | `mle-reviewer` |

### 3.4 After Writing Code

Auto-trigger **without user prompting**:
- Code written/modified → `code-reviewer` agent (ECC)
- Bug fixed → `tdd-guide` agent (ECC)
- Build failure → `build-error-resolver` agent (ECC)
- Security-sensitive code → `security-reviewer` agent (ECC)

---

## 🧪 PHASE 4 — TESTING & VERIFICATION

> Skill sources: **gstack** (/qa, /review) + **ECC** (e2e-runner, tdd-guide) + **karpathy-skills** (goal-driven execution)

### 4.1 Testing Requirements

- **80%+ code coverage** required for new features
- **Write tests first** for bug fixes (reproduce → fix → verify)
- **Non-trivial logic** → leave ONE runnable check behind (smallest thing that fails if logic breaks)
- **Trivial one-liners** → no test needed

### 4.2 Test Verification Loop

```
1. Write test that fails → verify failure is expected
2. Implement code
3. Run tests → verify all pass
4. Run security scan
5. Run type checks / linting
```

### 4.3 QA Checklist

```
☐ Unit tests pass
☐ Integration tests pass
☐ Type checks pass (mypy / tsc --noEmit)
☐ Linting clean (flake8 / eslint)
☐ No regression in existing tests
☐ Security reviewer approved
☐ Code reviewer approved
```

---

## 📖 PHASE 5 — DOCUMENTATION

> Skill sources: **obsidian-cli** (knowledge management) + **gstack** (/document-generate, /document-release) + **ECC** (doc-updater)

### 5.1 Documentation Standards

- **Always update README.md** after meaningful changes
- **Docstrings required** for all public functions/classes
- **Inline comments** for non-obvious logic (use `# Why:` prefix for intent)
- **Changelog entry** for every feature/fix using this format:

```markdown
## [Unreleased]
### Added
- Feature: Brief description
### Fixed
- Bug: Brief description (closes #issue)
### Changed
- Change: Brief description
```

### 5.2 Auto-Documentation

For large changes, trigger:
```
/document-generate    → Diataxis docs (tutorial/how-to/reference/explanation)
/document-release     → Update docs to match what was shipped
doc-updater agent     → Keeps codemaps and API docs current
```

### 5.3 Knowledge Base (Obsidian CLI)

If using Obsidian vault:
```bash
obsidian note create "feature/FEATURE-NAME" --content "..."
obsidian note append "daily-notes/$(date +%Y-%m-%d)" --content "## Done\n- FEATURE-NAME"
obsidian search "keyword" --vault MyVault
```

---

## 🚀 PHASE 6 — REVIEW & RELEASE

> Skill sources: **superpowers** (PR hygiene) + **gstack** (/review, /ship, /land-and-deploy) + **ECC** (code-reviewer, security-reviewer)

### 6.1 Pre-Commit Checklist

```
☐ All tests pass
☐ Security checklist completed (Phase 3.2)
☐ QA checklist completed (Phase 4.3)
☐ Documentation updated (Phase 5.1)
☐ No debugging code left in (print statements, console.logs, breakpoints)
☐ No TODO comments that block release
☐ git diff reviewed — every changed line traces to the user's request
```

### 6.2 PR Standards (Superpowers)

Every PR must include:
- **Real problem description** (not theoretical)
- **Root cause** identified
- **Solution approach** explained
- **Testing evidence** shown
- **Self-identification** if agent-generated (disclose model + harness)
- **No bundled unrelated changes**

### 6.3 Release Flow

```
/review              → Pre-landing PR review (finds prod bugs missed by CI)
/ship                → Run tests → review → push → open PR
/land-and-deploy     → Merge → wait for CI → verify production health
/canary              → Post-deploy monitoring loop
/document-release    → Update all docs
```

---

## 🔄 PHASE 7 — RETROSPECTIVE & LEARNING

> Skill sources: **gstack** (/retro, /health, /cso, /context-save) + **ruflo** (memory store)

### 7.1 After Completing Major Work

```
/context-save        → Save working context for resumption
/health              → Code quality dashboard (type checker, linter, tests, dead code)
/cso                 → OWASP Top 10 + STRIDE security audit
/retro               → Weekly retro with shipping streaks
```

### 7.2 Pattern Memory

After any successful implementation, store the pattern:
```
memory_store(key="pattern-<name>", value="what worked", namespace="patterns")
```

Before starting any task:
```
memory_search(query="task keywords")  → score > 0.7 = reuse the pattern
```

---

## 🎯 QUICK DECISION TREE

```
Incoming task
    │
    ├─► Bug report?
    │       ├─ Find root cause (ponytail: grep all callers)
    │       ├─ Write failing test first (karpathy-skills)
    │       ├─ Fix root, not symptom
    │       └─ Invoke: tdd-guide → code-reviewer → security-reviewer
    │
    ├─► New feature?
    │       ├─ Apply YAGNI ladder (ponytail)
    │       ├─ Plan first (planner agent / /autoplan)
    │       ├─ Design review if UI (ui-ux-pro-max + /plan-design-review)
    │       ├─ TDD implementation
    │       └─ Invoke: planner → tdd-guide → code-reviewer → security-reviewer → /review
    │
    ├─► Upgrade / migration?
    │       ├─ Read existing code fully before touching
    │       ├─ Architectural review (architect agent)
    │       ├─ Parallel execution for independent parts (ruflo)
    │       └─ Invoke: architect → code-reviewer → /health → /cso
    │
    ├─► UI/UX change?
    │       ├─ Search ui-ux-pro-max for styles, colors, typography
    │       ├─ /plan-design-review before implementing
    │       ├─ /design-review after implementing
    │       └─ /qa for live browser verification
    │
    └─► Documentation?
            ├─ /document-generate for new docs
            ├─ doc-updater agent for updates
            └─ obsidian-cli for vault management
```

---

## 📁 Sub-Skill Reference Paths

All sub-skills are stored at `.agents/skills/<name>/`. Read their files for detailed guidance:

| Skill | Path | Primary Files |
|-------|------|---------------|
| ponytail | `.agents/skills/ponytail/` | `AGENTS.md` |
| karpathy-skills | `.agents/skills/karpathy-skills/` | `CLAUDE.md`, `EXAMPLES.md` |
| ECC | `.agents/skills/ecc/` | `AGENTS.md`, `CLAUDE.md`, `COMMANDS-QUICK-REF.md` |
| gstack | `.agents/skills/gstack/` | `AGENTS.md`, `ARCHITECTURE.md` |
| superpowers | `.agents/skills/superpowers/` | `CLAUDE.md` |
| ui-ux-pro-max | `.agents/skills/ui-ux-pro-max/` | `CLAUDE.md` (search script: `src/ui-ux-pro-max/scripts/search.py`) |
| ruflo | `.agents/skills/ruflo/` | `AGENTS.md`, `CLAUDE.md` |
| obsidian-cli | `.agents/skills/obsidian-cli/skills/obsidian-cli/` | `SKILL.md`, `references/command-reference.md` |
| open-design | `.agents/skills/open-design/` | `AGENTS.md`, `CLAUDE.md` |

---

## ⚡ Core Principles Summary

| Principle | Source | Rule |
|-----------|--------|------|
| YAGNI ladder | ponytail | Always climb before writing |
| Simplicity first | karpathy + ponytail | 50 lines beats 200 always |
| Surgical changes | karpathy | Touch only what the request requires |
| Think before coding | karpathy | Surface assumptions → ask → then build |
| Test-driven | ECC | Tests before/with implementation |
| Security-first | ECC | Checklist before every commit |
| Plan before execute | ECC + gstack | Complex tasks get planned first |
| Agent orchestration | ECC + gstack | Right agent for the right task |
| Design intelligence | ui-ux-pro-max | Always query before writing CSS |
| PR hygiene | superpowers | Real problem, real solution, human review |
| Pattern memory | ruflo | Store and recall successful patterns |
| Documentation | obsidian + gstack | Always updated, never stale |
