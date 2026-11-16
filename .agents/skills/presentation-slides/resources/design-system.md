# Luis presentation design system

This document guides Codex when it creates or edits slides. The browser reads
[`assets/palettes.css`](../../../../assets/palettes.css), which is the live
source of colour values. Link that stylesheet **after** a deck's inline
`<style>` block. A deck in a talk folder uses `../assets/palettes.css`.

## Default palette

Read exact colour values from `assets/palettes.css`; avoid maintaining a second token table here.

Dark-mode body text is `#F6F8FD`; light-mode body text is slate `#323B4C`.
The supplied blue is a visual accent; light-mode accent **text** uses a darker
blue alias (`--orange`) so it can be read on white. `--orange` also keeps older
slide components working with the new palette. Prefer `--primary`, `--amber`,
and `--violet` in new CSS. Check contrast when putting coloured text on photos.

## Alternatives and configuration

`assets/palettes.css` contains a named `sunset` example. Set
`data-palette="sunset"` on a particular `<section class="slide">` to repeat
that slide with its message intact and different colours. Add new presets there
with both light and dark selectors. Record image, motion, typography and notes
choices in [`config/slide-presets.md`](../../../../config/slide-presets.md).
Avoid changing a whole deck when only one slide needs a variation.

## Canvas and typography

- The slide stage is fixed at 16:9 and letterboxed inside `.slides-viewport`.
  Target 1920 × 1080 for design review.
- Use `cqi` and `cqb` inside `.slides-stage`, with flex or percentage sizes where
  appropriate. Window units such as `vw` and `vh` can overflow a letterboxed
  slide. Run `scripts/lint-slides.mjs` when Node is available.
- Use Montserrat for prose and JetBrains Mono for labels/code, with system
  fallbacks. A suitable stage title is `clamp(24px, 3.7cqi, 54px)`; body copy
  should remain readable at a smaller browser size.
- Keep one main point per slide. Use primary blue for navigation and emphasis;
  amber and violet identify distinct ideas or route markers. Use restrained
  entrance animation and honor `prefers-reduced-motion`.

## Theme and reading modes

Every deck has a visible light/dark button and a visible reading-notes button.
Presentation mode hides `.detail` blocks; guide mode shows them for readers.
Neither mode hides the slide's essential title, image, or labels. Add a concise
description of a supplied image in `.detail` when it explains something the
visual alone cannot convey. Test both themes and both modes at 16:9 and a
smaller or taller window.

The presenter controls the same modes across its deck files. When a deck is
opened standalone, it starts with reading notes visible. Inside the presenter,
the default is the visual presentation mode.
