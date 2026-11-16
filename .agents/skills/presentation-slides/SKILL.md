---
name: presentation-slides
description: Create or edit this repository's static HTML slide decks, preserving the fixed stage, themes, navigation and presenter integration.
---

# Presentation slides

1. Identify the real talk folder. Read its `slide-guide.md` and optional `outline.md` before revising it. Example folder names are placeholders.
2. Reuse existing HTML for revisions. For new decks extract the complete HTML block from `starter/presentation-starter.txt`. Keep static HTML without a build step or dependencies just for editing slides.
3. Follow [design-system.md](resources/design-system.md). The live colours are in root `assets/palettes.css`; reusable non-colour choices belong in `config/slide-presets.md`.
4. For every change, maintain the complete implemented-slide record required by [slide-guide-spec.md](../../../config/slide-guide-spec.md). Copy root `starter/slide-guide-template.md` for a new talk. This includes tiny copy edits; a concise prompt log is insufficient.
5. Validate the HTML and guide together and report checks actually run and remaining uncertainties.

## Validation

From the root, replace `example-talk` with the actual folder:

```powershell
node .agents/skills/presentation-slides/scripts/lint-slides.mjs example-talk/01-intro.html
python scripts/check-slide-guide.py example-talk
```

Run with available runtimes; do not install software merely for checks. The sizing checker does not prove visual fit. The guide checker checks keys and static text only; inspect images, generated text and behaviour separately.

In a browser check large (1920 ? 1080) and smaller/taller viewports, both themes, both notes modes, assets, overflow, navigation boundaries, reveal steps, animation and reduced motion. Check standalone and presenter modes where applicable. Disclose checks unavailable in the current environment.

## Read references as needed

- [Guide specification](../../../config/slide-guide-spec.md): required for all slide work.
- [Design system](resources/design-system.md): stage sizing, typography, colour and notes.
- [Slide patterns](resources/slide-types.md) and [working examples](resources/slide-type-examples.html): optional layout ideas; adapt sizing to the stage.
- [Presenter reference](resources/presenter-reference.md): integration protocol, timing, optional features and export.
- [Presenter template](resources/presenter-template.html): copy for a new presenter and fill TITLE, HEADER_TITLE, LOGOS, PLAYLIST and PDF. Root `presenter.config.js` holds feature flags; PLAYLIST holds deck order and timing.

Standalone decks have visible theme, notes and navigation controls. Embedded decks hide duplicate chrome and accept presenter commands. Preserve both modes.
