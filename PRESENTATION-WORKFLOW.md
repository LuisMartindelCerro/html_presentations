# Create or revise a talk

1. Choose an actual folder name and supply audience, message, facts and assets. Example names below are placeholders.
2. For a new deck extract the complete HTML block from `starter/presentation-starter.txt` into `<talk>/01-intro.html`. Reuse existing HTML for revisions. Keep media paths relative.
3. Copy `starter/slide-guide-template.md` to `<talk>/slide-guide.md`; maintain it according to [the specification](config/slide-guide-spec.md). Keep an optional `outline.md` for the story map.
4. For a multi-deck talk copy the skill's `resources/presenter-template.html` and fill its five placeholders. Set order/labels/minutes in PLAYLIST and feature flags in root `presenter.config.js`.
5. Inspect HTML and guide together using the skill's validation checklist. Report remaining unverified pieces.

Example request:

> Use the presentation-slides skill to create six slides in example-talk/ for [audience] about [topic], using these facts/assets: [...]. Deliver HTML and a complete slide-guide.md following config/slide-guide-spec.md.

Every revision updates the same guide entry in the same task.

## Checks

Run from the root with available runtimes:

```powershell
node .agents/skills/presentation-slides/scripts/lint-slides.mjs example-talk/01-intro.html
python scripts/check-slide-guide.py example-talk
```

These are partial checks. Full review requirements live in the skill and guide specification.

## Optional PDF export

With Node.js available, install export dependencies only when needed:

```powershell
cd scripts
npm ci
node export-pdf.mjs example-talk
```

The exporter reads the real talk's presenter PLAYLIST. Use `--density=guide` for reading notes or `--theme=light`. Configure the PDF filename in the presenter to expose its download button. Integration details live in the skill's presenter reference.
