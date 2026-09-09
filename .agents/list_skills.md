# 📚 SYNXA Skills Command Reference

> **Complete guide** to all installed skills and how to invoke them for specific tasks.
> Skills are stored in `.agents/skills/` in this workspace.

---

## 🗂️ Installed Skills Index

| # | Skill | Repo | Primary Use |
|---|-------|------|-------------|
| 1 | **superpowers** | obra/superpowers | PR hygiene, agent contribution standards |
| 2 | **ECC** | affaan-m/ECC | 68 specialized agents, 94 commands, TDD |
| 3 | **ruflo** | ruvnet/ruflo | Multi-agent coordination, memory patterns |
| 4 | **open-design** | nexu-io/open-design | Design systems, component architecture |
| 5 | **obsidian-cli** | pablo-mano/Obsidian-CLI-skill | Knowledge base, vault operations |
| 6 | **karpathy-skills** | multica-ai/andrej-karpathy-skills | Coding discipline, simplicity-first |
| 7 | **ponytail** | DietrichGebert/ponytail | Lazy senior dev mode, YAGNI |
| 8 | **ui-ux-pro-max** | nextlevelbuilder/ui-ux-pro-max-skill | Design intelligence, CSS/UI lookup |
| 9 | **gstack** | garrytan/gstack | Full engineering workflow, 30+ commands |

---

## 🎯 Task-Based Quick Reference

### 🐛 Bug Fixes
```
Mention: "bug", "fix", "error", "broken", "not working"
→ Auto-loads: ponytail (root cause) + karpathy-skills (test first) + ECC (tdd-guide)

Agents to invoke:
  - tdd-guide          → Write failing test reproducing the bug first
  - investigate        → Systematic root-cause debugging (gstack)
  - code-reviewer      → After fix is written
  - security-reviewer  → If bug is security-related
```

### ✨ New Features
```
Mention: "add", "create", "implement", "build", "new feature"
→ Auto-loads: All phases of master SKILL.md

Agent chain:
  1. planner           → Implementation plan (ECC)
  2. architect         → If architectural decision involved (ECC)
  3. tdd-guide         → Write tests first (ECC)
  4. code-reviewer     → After implementation (ECC)
  5. security-reviewer → Before commit (ECC)
  6. /review           → Pre-landing review (gstack)
```

### 🏗️ Architecture & Refactoring
```
Mention: "refactor", "restructure", "architecture", "migrate", "upgrade"
→ Loads: ECC architect + ruflo coordination + gstack /health

Commands:
  /autoplan            → CEO → design → DX → eng review pipeline
  /spec                → Turn vague request into precise executable spec
  /health              → Code quality dashboard before starting
  architect agent      → Architectural decision making
  refactor-cleaner     → Dead code cleanup after refactor
```

### 🎨 UI / Frontend / Design
```
Mention: "UI", "design", "CSS", "component", "page", "layout", "style"
→ Loads: ui-ux-pro-max + open-design + gstack design skills

UI/UX Search Commands:
  python3 .agents/skills/ui-ux-pro-max/src/ui-ux-pro-max/scripts/search.py "<query>" --domain style
  python3 .agents/skills/ui-ux-pro-max/src/ui-ux-pro-max/scripts/search.py "<query>" --domain color
  python3 .agents/skills/ui-ux-pro-max/src/ui-ux-pro-max/scripts/search.py "<query>" --domain typography
  python3 .agents/skills/ui-ux-pro-max/src/ui-ux-pro-max/scripts/search.py "<query>" --domain ux
  python3 .agents/skills/ui-ux-pro-max/src/ui-ux-pro-max/scripts/search.py "<query>" --domain gsap
  python3 .agents/skills/ui-ux-pro-max/src/ui-ux-pro-max/scripts/search.py "<query>" --domain chart
  python3 .agents/skills/ui-ux-pro-max/src/ui-ux-pro-max/scripts/search.py "<query>" --domain icons

  # With design system dials (variance 1-10, motion 1-10, density 1-10):
  python3 .agents/skills/ui-ux-pro-max/src/ui-ux-pro-max/scripts/search.py "<query>" \
    --design-system --variance 8 --motion 7 --density 5

  # With specific stack:
  python3 .agents/skills/ui-ux-pro-max/src/ui-ux-pro-max/scripts/search.py "<query>" --stack react

Gstack design commands:
  /design-consultation → Build complete design system from scratch
  /plan-design-review  → Rate each design dimension 0-10 before building
  /design-review       → Live-site visual audit + fix loop
  /design-shotgun      → Generate multiple AI design variants, pick best
  /design-html         → Generate production-quality HTML/CSS
  /qa                  → Open real browser, find bugs, fix, re-verify
```

### 🔒 Security Audit
```
Mention: "security", "vulnerability", "auth", "sensitive", "secrets"
→ Loads: ECC security-reviewer + gstack /cso

Commands:
  security-reviewer    → Full vulnerability detection (ECC)
  /cso                 → OWASP Top 10 + STRIDE security audit (gstack)
```

### 🧪 Testing
```
Mention: "test", "coverage", "TDD", "unit test", "e2e"
→ Loads: ECC tdd-guide + e2e-runner

Commands:
  tdd-guide            → TDD workflow guidance (ECC)
  e2e-runner           → End-to-end Playwright testing for critical flows (ECC)
  /qa                  → Browser-based QA with fix loop (gstack)
  /qa-only             → Browser QA report only, no code changes (gstack)
```

### 📖 Documentation
```
Mention: "docs", "documentation", "README", "comment", "explain"
→ Loads: gstack /document-generate + ECC doc-updater + obsidian-cli

Commands:
  /document-generate   → Generate Diataxis docs from code (gstack)
  /document-release    → Update all docs after shipping (gstack)
  doc-updater          → Keep codemaps and API docs current (ECC)

Obsidian CLI (vault management):
  obsidian note create "path/note-name" --content "..."
  obsidian note read "path/note-name"
  obsidian note append "path/note-name" --content "..."
  obsidian note prepend "path/note-name" --content "..."
  obsidian search "keyword" --vault VaultName
  obsidian tasks list --status open
  obsidian tasks check "task text"
  obsidian note move "old/path" "new/path"
  obsidian note delete "path/note-name"
```

### 🚀 Deploy & Release
```
Mention: "deploy", "release", "ship", "PR", "merge", "production"
→ Loads: gstack /ship + superpowers PR hygiene

Commands:
  /review              → Pre-landing PR review (gstack)
  /ship                → Run tests → review → push → open PR (gstack)
  /land-and-deploy     → Merge PR → wait CI → verify production (gstack)
  /canary              → Post-deploy monitoring loop (gstack)
  /setup-deploy        → One-time deploy config detection (gstack)
  /document-release    → Update docs post-ship (gstack)
```

### 🔍 Code Review
```
Mention: "review", "check my code", "quality", "PR review"
→ Loads: ECC code-reviewer + gstack /review

Commands:
  code-reviewer        → Code quality and maintainability review (ECC)
  /review              → Pre-landing PR review, finds prod bugs (gstack)
  /codex               → Second opinion via OpenAI Codex (gstack)
```

### 🗄️ Database / Backend
```
Mention: "database", "SQL", "PostgreSQL", "API", "backend", "schema"
→ Loads: ECC database-reviewer + relevant language reviewers

Agents:
  database-reviewer    → PostgreSQL/Supabase specialist (ECC)
  python-reviewer      → Python code review (ECC)
  django-reviewer      → Django/DRF/ORM/migrations review (ECC)
  typescript-reviewer  → TypeScript/JavaScript review (ECC)
  java-reviewer        → Java/Spring Boot review (ECC)
  go-reviewer          → Go code review (ECC)
  rust-reviewer        → Rust code review (ECC)
```

### 🤖 AI/ML Features
```
Mention: "ML", "AI", "model", "training", "RAG", "pipeline", "LLM"
→ Loads: ECC mle-reviewer + rag-pipeline-reviewer

Agents:
  mle-reviewer         → Production ML pipeline review (ECC)
  rag-pipeline-reviewer → RAG pipeline, retrieval quality, RAGAS eval (ECC)
  pytorch-build-resolver → PyTorch/CUDA/training errors (ECC)
```

### ⚡ Performance
```
Mention: "slow", "performance", "optimize", "speed", "bottleneck"
→ Loads: gstack /benchmark + ui-ux-pro-max react domain

Commands:
  /benchmark           → Performance regression detection (gstack)
  /benchmark-models    → Cross-model benchmark for skills (gstack)

UI performance:
  python3 ... search.py "performance" --domain react
```

### 🧹 Code Health & Maintenance
```
Mention: "cleanup", "dead code", "tech debt", "maintenance"
→ Loads: ECC refactor-cleaner + gstack /health

Commands:
  refactor-cleaner     → Dead code cleanup (ECC)
  /health              → Code quality dashboard: types, linter, tests, dead code (gstack)
  /retro               → Weekly retro with shipping streaks (gstack)
```

### 💾 Session Memory & Context
```
Mention: "remember", "context", "resume", "continue from"
→ Loads: gstack /context-save + ruflo memory system

Commands:
  /context-save        → Save working context, git state, decisions (gstack)
  /context-restore     → Resume from saved context across sessions (gstack)
  /learn               → Manage what gstack learned (gstack)

Ruflo memory:
  memory_search(query="task keywords")                        # Search before starting
  memory_store(key="pattern-X", namespace="patterns", ...)   # Store after success
```

---

## 🤖 ECC Agent Quick Reference (68 specialized agents)

### Planning & Architecture
| Agent | Command | When |
|-------|---------|------|
| planner | `planner: <task>` | Complex features, refactoring |
| architect | `architect: <decision>` | System design, scalability |
| spec-miner | `spec-miner` | Brownfield project onboarding |

### Code Quality
| Agent | Command | When |
|-------|---------|------|
| code-reviewer | `code-reviewer` | After writing/modifying code |
| tdd-guide | `tdd-guide: <feature>` | New features, bug fixes |
| refactor-cleaner | `refactor-cleaner` | Code maintenance |
| build-error-resolver | `build-error-resolver` | Build failures |

### Security
| Agent | Command | When |
|-------|---------|------|
| security-reviewer | `security-reviewer` | Before commits, sensitive code |

### Language Specialists
| Agent | When |
|-------|------|
| python-reviewer | Python projects |
| typescript-reviewer | TypeScript/JS |
| go-reviewer | Go projects |
| rust-reviewer | Rust |
| java-reviewer | Java/Spring |
| django-reviewer | Django/DRF |
| database-reviewer | PostgreSQL/SQL |
| cpp-reviewer | C/C++ |
| fsharp-reviewer | F# |
| kotlin-reviewer | Kotlin/Android |

### ML/AI
| Agent | When |
|-------|------|
| mle-reviewer | ML pipelines |
| rag-pipeline-reviewer | RAG/retrieval |
| pytorch-build-resolver | PyTorch errors |

### DevOps
| Agent | When |
|-------|------|
| doc-updater | Documentation |
| e2e-runner | E2E Playwright tests |
| loop-operator | Autonomous loops |
| harness-optimizer | Harness config tuning |
| docs-lookup | API/docs questions |

---

## 🛠️ Gstack Command Quick Reference (30+ commands)

### Planning (Use Before Building)
```
/office-hours         → Reframe product idea before writing code
/plan-ceo-review      → CEO-level: find the 10-star product in the request
/plan-eng-review      → Lock architecture, data flow, edge cases, tests
/plan-design-review   → Rate each design dimension 0-10
/plan-devex-review    → DX: TTHW, magical moments, friction points
/autoplan             → One command: CEO → design → DX → eng review
/spec                 → Turn vague intent into precise executable spec
/design-consultation  → Build complete design system from scratch
```

### Implementation & Review
```
/review               → Pre-landing PR review
/investigate          → Systematic root-cause debugging
/design-review        → Live-site visual audit + fix loop
/design-shotgun       → Generate multiple AI design variants
/design-html          → Production-quality HTML/CSS generation
/devex-review         → Developer experience audit
/qa                   → Real browser QA: find bugs, fix, re-verify
/qa-only              → Browser QA report only
/codex                → Second opinion via OpenAI Codex
/browse               → Drive browser: navigate, click, screenshot
/scrape               → Pull data from web page
```

### Release & Deploy
```
/ship                 → Tests → review → push → open PR
/land-and-deploy      → Merge PR → CI → verify production
/canary               → Post-deploy monitoring
/landing-report       → Ship queue dashboard
/document-release     → Update docs post-ship
/document-generate    → Generate Diataxis docs from code
/setup-deploy         → One-time deploy config (Fly.io, Render, Vercel, etc.)
```

### Operational
```
/context-save         → Save working context
/context-restore      → Resume from saved context
/learn                → Manage session learning
/retro                → Weekly retro with shipping streaks
/health               → Code quality dashboard
/benchmark            → Performance regression detection
/cso                  → OWASP + STRIDE security audit
/gstack-upgrade       → Update gstack to latest version
```

---

## 📐 Ponytail Rules (Applied to Every Task)

```
The YAGNI Ladder (climb before writing):
  1. Does this need to be built at all?
  2. Does it already exist in this codebase? → Reuse it
  3. Does stdlib already do this? → Use it
  4. Does an installed dep solve it? → Use it
  5. Can it be one line? → Make it one line
  6. Only then: write minimum code that works

Key rules:
  ✓ No abstractions unless explicitly requested
  ✓ No new dependency if avoidable
  ✓ No boilerplate nobody asked for
  ✓ Deletion over addition
  ✓ Boring over clever
  ✓ Shortest working diff wins
  ✓ Mark deliberate simplifications: ponytail: <ceiling> / upgrade: <path>
```

---

## 🧠 Karpathy-Skills Rules (Applied to Every Session)

```
Principle 1 — Think Before Coding:
  → State assumptions explicitly
  → If multiple interpretations exist, list them → ask
  → If simpler approach exists, say so and push back

Principle 2 — Simplicity First:
  → Minimum code that solves the problem
  → No speculative features
  → No abstractions for single-use code
  → "Would a senior engineer say this is overcomplicated?" → If yes, simplify

Principle 3 — Surgical Changes:
  → Don't "improve" adjacent code
  → Match existing style even if you'd do it differently
  → Every changed line must trace directly to the user's request

Principle 4 — Goal-Driven Execution:
  → Transform tasks into verifiable goals
  → "Fix the bug" → "Write test reproducing it, then make it pass"
  → State plan before multi-step tasks
```

---

## 📍 Skill File Locations

```
Workspace root: C:\Users\sreej\OneDrive\Desktop\SYNXA-LEARN\

Master skill:     .agents\SKILL.md
This file:        .agents\list_skills.md

Sub-skills:
  .agents\skills\superpowers\         obra/superpowers
  .agents\skills\ecc\                 affaan-m/ECC
  .agents\skills\ruflo\               ruvnet/ruflo
  .agents\skills\open-design\         nexu-io/open-design
  .agents\skills\obsidian-cli\        pablo-mano/Obsidian-CLI-skill
  .agents\skills\karpathy-skills\     multica-ai/andrej-karpathy-skills
  .agents\skills\ponytail\            DietrichGebert/ponytail
  .agents\skills\ui-ux-pro-max\       nextlevelbuilder/ui-ux-pro-max-skill
  .agents\skills\gstack\              garrytan/gstack
```

---

## 🔄 Update Skills

To pull the latest version of any skill:
```powershell
# Update a single skill
cd .agents\skills\ponytail; git pull

# Update all skills at once
Get-ChildItem .agents\skills -Directory | ForEach-Object {
    Write-Host "Updating $($_.Name)..."
    git -C $_.FullName pull
}
```
