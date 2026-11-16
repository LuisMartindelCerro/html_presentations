# Slide configurations

The default colours live in `../assets/palettes.css`. That file is loaded by
decks and presenters, so edits there affect both light and dark modes. The
specified primary blue is `#56BFFA`; light-mode accent *text* uses a darker
derived blue for readability on white. Dark-mode text is light even though the
palette's slate swatch remains `#323B4C`.

For one alternate slide, add `data-palette="sunset"` to its `<section
class="slide">`. The named preset is defined at the bottom of the CSS file.
Duplicate and rename that block for another colour set. Keep a light and dark
version and check contrast in both. The deck-level toolbar keeps the default
palette so its controls remain consistent.

Use this file to describe design choices beyond colour. Codex should apply the
named configuration only to the slide requested and preserve its message.

| Preset | Colour | Images | Motion | Notes |
| --- | --- | --- | --- | --- |
| `default` | Luis light/dark palette | Full image or clean crop | Gentle fade or staggered reveal | Presenter's stage/guide switch |
| `sunset` | Warm alternate in `palettes.css` | One dominant image | Short fade | Same stage/guide switch |
| `signum-orbit` | Default palette from `palettes.css`; retain supplied logo colours | Supplied monochrome skill icons and two matching SVG pictograms, each with a thin circular outline; darken icons in light mode for contrast | Arrow-driven elliptical rotation in 650 ms; six skills wrap in either direction; no autoplay; reduced motion changes selection immediately | Show the selected skill's full description with Notes On; retain its name, short summary and arrows with Notes Off |


Talk-specific layout and motion belong in that talk's `slide-guide.md`. Add only reusable presets here.

Example prompt: “Repeat slide 3 with the `sunset` configuration. Keep the text
and image, use a slower image fade, and update the complete entry in the talk's slide-guide.md.”

For a new named configuration, tell Codex the palette values for both modes,
image treatment, typography, and animation. Codex should add the CSS preset here
and describe it in this table before applying it to a slide.
