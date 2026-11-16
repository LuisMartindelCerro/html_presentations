# Complete slide guide specification

Every talk has one `slide-guide.md`: the authoritative human-readable description of the implemented slides. A reader must understand every piece, literal text and behaviour without opening the HTML. It is separate from the HTML's reading-notes mode.

## Entry identity

Use one unique heading per slide: `## ` followed by the deck filename in backticks and `/ data-slide="N"`. Paths are relative to the guide. Update keys after renaming or renumbering; remove deleted-slide entries. Document shared controls once in a shared section and describe slide exceptions. Mark planned slides separately from implemented slides.

An optional `outline.md` is a short story map. Existing prompt logs may remain as history, but new talks do not require a second per-slide prompt record. Neither an outline nor a prompt summary substitutes for the guide.

## Required content per slide

1. **Purpose and meaning:** explain the message, factual basis and what each element communicates.
2. **Exact literal text:** transcribe every title, subtitle, paragraph, label, caption, legend, table cell, code block, number, unit, footer, citation label, link, tooltip, button and reading note. Include initially hidden and later revealed text and every discrete control state. Preserve punctuation, capitalization and wording. Group by element/state, using fenced text blocks. Transcribe meaningful text inside charts, images and screenshots too; identify genuinely illegible text rather than inventing it.
3. **Visual inventory and layout:** describe every image, chart, diagram, icon, shape and decorative piece. Give asset paths, alt text, provenance, placement, relative size, crop, palette and meaning. Explain axes, encodings and illustrative values. Record shared presets and local overrides.
4. **Initial state and ordered states:** specify entry visibility, every forward/reverse reveal, triggers, resulting states, and reset/persistence on re-entry.
5. **Animation:** identify each element, trigger, order, delay, duration, easing, movement, repetition, stopping/reset and reduced-motion behaviour. Explicitly state when there is no motion.
6. **Interaction and generated content:** document keyboard commands, clicks, hovers, drags, sliders, buttons and link destinations. Record all exact discrete labels. For continuous values record formulas, ranges, defaults, units and formatting. Include empty/loading/error states if implemented.
7. **Theme and density:** explain light/dark, notes on/off, responsive and standalone/presenter differences. Include the full reading-note transcript.
8. **Evidence and validation:** cite URLs/assets, distinguish measured facts from illustrative examples, and list checks actually run, viewports/modes and remaining limitations.

## Update and verification

Read the guide before editing. Update HTML and the matching entry in the same task for every copy, asset, style, state, interaction or motion revision. Reconcile requested results with actual implementation; do not silently describe intended behaviour as verified behaviour.

Before finishing, compare slide keys and literal text with the guide; inspect assets and generated states; walk interactions and animations where possible. Run `python scripts/check-slide-guide.py <talk-folder>` for partial static coverage. It cannot certify layout, image transcription, generated content, or animation descriptions. Report unavailable checks and never claim complete verification from the checker alone.

Start from `starter/slide-guide-template.md`. Example filenames are placeholders.
