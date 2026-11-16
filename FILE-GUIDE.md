# Repository file guide

| Location | Responsibility |
| --- | --- |
| `README.md` | Human entry point and links. |
| `AGENTS.md` | Brief project rules and routing for AI agents. |
| `PRESENTATION-WORKFLOW.md` | Human workflow and commands. |
| `.agents/skills/presentation-slides/SKILL.md` | Authoring workflow and reference routing. |
| `config/slide-guide-spec.md` | Canonical complete-documentation requirements. |
| `starter/slide-guide-template.md` | Blank per-talk implementation record. |
| `<talk>/slide-guide.md` | Exact implemented text, visuals, states, motion, controls and validation. |
| `<talk>/outline.md` | Optional story map. |
| `<talk>/*.html` and media | Actual slides, optional presenter/landing page and assets. |
| `starter/presentation-starter.txt` | Portable instructions, complete HTML and optional checker; intentionally self-contained. |
| Skill `resources/design-system.md` | Visual authoring guidance. |
| `assets/palettes.css` | Executable shared colour values and named variations. |
| `config/slide-presets.md` | Reusable non-colour choices. |
| Skill `resources/slide-types.md` and `slide-type-examples.html` | Layout patterns and runnable examples. |
| Skill `resources/presenter-template.html` | Master presenter template; existing copies do not update automatically. |
| Skill `resources/presenter-reference.md` | Integration protocol, timing, optional features and PDF notes. |
| Skill `resources/boilerplate.md` | Compatibility pointer to the complete starter. |
| Skill `scripts/lint-slides.mjs` | CSS sizing checker. |
| `scripts/check-slide-guide.py` | Partial static slide-key and text-coverage checker. |
| `scripts/export-pdf.mjs`, `scripts/package*.json` | Optional PDF exporter and dependencies. |
| `presenter.config.js` | Shared feature flags and actual per-talk overrides. |
| `assets/talklog.js`, `assets/copresenter-bridge.js` | Optional presenter integrations. |
| `.gitignore` | Local dependency, log and private-talk exclusions. |

Prompt logs are optional history, not another required implementation record. Link shared requirements rather than repeating them. The portable starter duplicates essential rules because it must work outside the repository.
