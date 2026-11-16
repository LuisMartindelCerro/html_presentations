# Presenter and export reference

Example folder names are placeholders; create the talk first.

## Presenter / Playlist Navigator

Each presentation folder can have a `presenter.html` that sequences standalone decks via iframes:

```
presenter.html          ← Open this for the full talk
  ├── 01-entropy.html   ← Loaded in iframe, standalone too
  ├── 02-authority.html
  └── 03-future.html
```

**Feature flags live in `presenter.config.js` at the repo root**, not in the presenter. It sets repo-wide `defaults` and per-talk overrides keyed by folder name:

```js
window.PRESENTER_CONFIG = {
  defaults: { picker: true, timer: true, density: true, pdf: true, talklog: false },
  talks: { 'example-talk': { talklog: true } },
};
```

Flags are for turning features on and off while trying them out. Deck order, labels and `minutes` stay in each talk's PLAYLIST — that's the shape of the talk, not a toggle. The presenter carries the same defaults inline as a fallback, so a missing config file degrades to a working deck rather than a blank page.

**Never hand-write a presenter.** Copy `resources/presenter-template.html` and fill its five placeholders — `{{TITLE}}`, `{{HEADER_TITLE}}`, `{{LOGOS}}`, `{{PLAYLIST}}`, `{{PDF}}`. It is the single source of the deck picker, theme sync, density toggle, timer and PDF button; every deck folder in this repo is an instance of it. Fixing a presenter bug means fixing the template and re-instantiating, not patching five copies.

**Keyboard navigation:**
- **← →** — Navigate slides/steps within a deck only (never crosses deck boundaries). The presenter forwards them as `{type:'deck-command', action:'next'|'prev'}`, so they work whether focus is in the deck or on the presenter chrome; its bottom bar also has slide buttons and a counter fed by `deck-slide`. A deck must handle `next`/`prev` or it only moves when clicked into.
- **↑ ↓** — Jump between decks (↓ = next deck, ↑ = previous deck)
- **D** — Toggle detail density (stage ↔ guide) across every deck
- **Esc** — Close the deck jump menu

**How it works:**
- Each deck stays self-contained — works fine opened directly in a browser
- ←/→ only navigate within a deck; they stop at the first/last slide
- When embedded, decks communicate via `postMessage`:
  - ↑/↓ keys: posts `{type:'deck-nav', dir:'next'|'prev'}` → presenter switches decks
  - Theme syncs across all decks via `{type:'deck-command', action:'set-theme', theme:'light'}`
  - Density syncs the same way via `{type:'deck-command', action:'set-density', density:'stage'|'guide'}`; a deck whose own **D** key was pressed reports back up with `{type:'deck-density', density}` so the presenter's button stays in sync
- Playlist order is a simple JS array — edit to reorder/include/exclude per audience:

```js
const PLAYLIST = [
  { src: '01-entropy-explorer.html', label: 'Entropy',   minutes: 3, group: 'Talk' },
  { src: '02-authority-complexity.html', label: 'Authority', minutes: 6, group: 'Talk' },
];
```

`minutes` drives the timer (0 = off-clock). `group` is optional and becomes a heading in the jump menu — use it for workshop blocks, acts, or an appendix.

### Deck picker

The current-deck control sits in the middle of the top bar: prev/next arrows, the names of the adjacent decks either side, and a centre pill showing `n / total` plus the current label. Clicking the pill opens a popover jump menu grouped by `group`, with each deck's minute budget on the right.

It is deliberately **space-stable** — the menu is a popover, so opening it never reflows the bar mid-talk, and the neighbour labels are width-capped with ellipsis. This replaced a row of tabs, which stopped working past about six decks (the Croatia workshop ran seventeen).

Standalone decks retain theme, notes and navigation controls; hide duplicate chrome only when embedded.

**Adding postMessage bridge to a new deck:**

Add to the keyboard handler — ←/→ stay within deck, ↑/↓ signal parent:
```js
document.addEventListener('keydown', e=>{
  if(e.key==='ArrowRight'||e.key===' ') goTo(current+1);
  if(e.key==='ArrowLeft') goTo(current-1);
  // ↑/↓ = deck-level navigation (handled by parent presenter)
  if(e.key==='ArrowDown'){ e.preventDefault(); window.parent.postMessage({type:'deck-nav',dir:'next'},'*'); }
  if(e.key==='ArrowUp'){ e.preventDefault(); window.parent.postMessage({type:'deck-nav',dir:'prev'},'*'); }
});
```

Add message listener for presenter commands (theme sync, jump to first/last):
```js
window.addEventListener('message', e=>{
  if(e.data && e.data.type==='deck-command'){
    if(e.data.action==='go-first') goTo(0);
    if(e.data.action==='next') goTo(current+1);
    if(e.data.action==='prev') goTo(current-1);
    if(e.data.action==='go-last'){ current=-1; goTo(TOTAL-1); }
    if(e.data.action==='set-theme') setTheme(e.data.theme);
  }
});
```

## Detail Density: Stage vs Guide

The same deck serves two very different readers — the room, which needs a sparse slide behind a talking human, and the person who opens the published link cold weeks later with no narration. Density is how one file serves both.

Wrap take-home prose in `class="detail"`:

```html
<div class="stat">−66.7 → +4.5</div>
<p class="detail">That's AILANG's LoCoBench delta against Python between v0.6 and v0.9 —
   the point where an AI-first language stopped being a toy.</p>
```

Two modes:
- **stage** — `.detail` hidden. What the projector shows.
- **guide** — `.detail` revealed. The laptop view, and the default for anyone opening the deck standalone.

The whole mechanism, already wired into every deck by the boilerplate:

```css
html[data-density="stage"] .detail{display:none}
```
```js
var embedded = window !== window.top, root = document.documentElement;
root.setAttribute('data-density', embedded ? 'stage' : 'guide');
```

That one line is the important bit: **in the presenter iframe it defaults to stage; opened directly it defaults to guide.** So the deck the room sees stays clean, and the same URL on sunholo.com explains itself to a stranger with no extra file to maintain.

Toggle it with **D** (in either the presenter or a standalone deck), or the ◦ button in the presenter's top-right, which broadcasts to every loaded deck at once. The presenter remembers the choice in `localStorage` under `presenter-density`.

**Authoring rules:**
- Design the slide for **stage** first. `.detail` is additive — a slide must never depend on it to make sense.
- Keep `.detail` prose to a sentence or two, and give it somewhere to go: a slide that's already full in stage mode will overflow in guide mode. Prefer a footer strip or a column that's empty on stage.
- Never put a `.detail` block inside a `data-steps` reveal sequence — the step counter won't know about it.
- Check both modes before shipping. The linter can't see layout overflow.

## Talk Log (flag: `talklog`)

`assets/talklog.js`, loaded only when the flag is on. Captures what actually happened during a talk so the write-up afterwards isn't reconstructed from memory.

- **Q** — capture an audience question, tagged with the deck and slide on screen
- **N** — capture a note to self
- **L** — open the log: timing table, slowest slides, captured entries, markdown export

The export is the point. It gives you the questions with the slide that prompted them, the slowest slides, and a ready-to-paste block of `minutes:` values measured from a real run — so the next delivery is budgeted from evidence rather than a guess.

State persists in `localStorage` under `talklog:<folder>`, so a mid-talk refresh loses nothing. Clear it before a repeat delivery, or you'll append to the previous run.

### How slide timing works without touching decks

Slide-level timing needs to know which slide is showing. Rather than hooking every deck's `goTo()`, the deck-side bridge watches for `.slide.active` changing with a `MutationObserver` and posts `{type:'deck-slide', index, total}` to the presenter. Decks don't know the talk log exists.

Decks that aren't slide-based (the entropy explorer steps through scenarios, not `.slide` elements) simply report nothing and degrade to deck-level timing.

### Hotkeys and iframe focus

During a talk keyboard focus sits **inside the deck iframe**, so a `keydown` listener in the presenter never fires. The deck-side bridge relays the keys a deck doesn't use itself — `d`, `q`, `n`, `l` — up as `{type:'deck-hotkey', key}`. The presenter is the single authority: it acts on the key and broadcasts the result back down.

If you add a presenter-level hotkey, add it to the relay list in the boilerplate too, or it will only work when focus happens to be on the presenter chrome. Both the relay and the presenter's own handler skip events originating in an `INPUT` or `TEXTAREA`, so typing a question doesn't trigger anything.

## AI Co-Presenter (flag: `copresenter`)

A headset button in the top bar opens the AILANG co-presenter in a second window — your laptop, while the deck is on the projector. It listens to the room through Gemini Live, researches in the background, and shows a trace of every tool call.

**It is a bridge, not a port, and that was a deliberate call.** The co-presenter lives at `sunholo.com/ailang-demos/co-presenter/` because its Gemini Live session is driven by AILANG WASM — `ailang.wasm` alone is 39MB, plus `gemini-live-core.js` and four `pkg/sunholo/gemini_live/*.ail` modules. Copying that here would double the repo and fork the AILANG stack. So `assets/copresenter-bridge.js` opens the deployed app and talks to it over `postMessage`.

That also fixes the reason the two never worked together before. The co-presenter's `getSlideContext` tool read `frame.contentDocument`, which is same-origin only — point it at a deck on another origin and it silently returned *"No slide context available."* postMessage has no such limit, so the presenter now pushes what's on screen:

```
presenter → copresenter   presenter-hello       handshake, retried until answered
                          presenter-context     { talk, title, deck, slide{index,total,title,text} }
copresenter → presenter   copresenter-ready     it's listening
                          copresenter-entry     { kind:'q'|'n', text } → into the talk log
```

The last one is the nice part: a question the model logs through its `audienceQuestion` tool lands in the same markdown export as the ones you typed by hand.

Messages are addressed to the exact origin from `copresenterUrl` and inbound ones are checked against it. Never widen either to `'*'` — that window holds a Gemini API key.

### Two failure modes worth knowing

**`innerText` is layout-dependent.** Read a slide the instant its `.active` class lands and you get an empty string, because the transition hasn't been laid out yet. The bridge waits 160ms and falls back to `textContent`. If you see empty slide context, that's the place to look.

**A deck that doesn't change slide never reports.** Switching decks used to leave the presenter describing the *previous* deck's slide indefinitely. The presenter now clears its cached slide on every switch and sends `{action:'report-slide'}` to the incoming deck, which forces a fresh report.

Decks that aren't slide-based (the entropy explorer steps through scenarios, not `.slide` elements) report `index: -1` and send the whole view's text instead, so the model still knows what's on screen.

## PDF Export

`scripts/export-pdf.mjs` produces a faithful PDF of any deck folder — one landscape page per slide.

```bash
cd scripts && npm ci            # one-time, downloads a Chromium
node export-pdf.mjs example-talk
node export-pdf.mjs example-talk --density=guide   # include .detail prose
node export-pdf.mjs example-talk --only=01-intro.html --scale=1
```

It is **not** `@media print`, and it can't be: decks stack slides absolutely with only `.active` visible, reveal content through CSS animations starting at `opacity:0`, and build some slides up over several `data-steps` presses. A static print captures none of that. So the script drives the real decks in headless Chrome, walks each slide to its final revealed step, screenshots at 1920×1080, and assembles the images into one PDF.

- Deck order comes from that folder's `PLAYLIST`, so the PDF can never drift from the live deck order.
- Defaults to `--density=stage` (faithful to the room). Pass `--density=guide` for a take-home handout that includes the detail prose.
- Output lands at `<folder>/<folder>.pdf`. To expose the download button, set `const PDF = '<folder>.pdf'` next to the PLAYLIST in that folder's `presenter.html` — leave it `null` and the button stays hidden.
- Roughly 250KB per slide at the default 2× scale. Only commit PDFs for talks that are actually published.

### Embed-aware chrome (fixes "inner page too high")

A deck keeps its own `.top-bar` and `.bottom-bar` so it still works standalone. But inside the presenter iframe, those bars duplicate the presenter's own chrome and steal vertical space from `.slides-viewport` — the bottom of slide content ends up clipped. Since `html,body{overflow:hidden}`, no scrollbar appears; it just looks wrong.

**Fix:** detect embedded mode and hide the deck's own bars.

```html
<script>if(window!==window.top)document.body.classList.add('in-iframe');</script>
```
```css
.in-iframe .top-bar{display:none}
.in-iframe .bottom-bar{display:none}
```

Standalone viewing is unchanged (the class only sets when `window !== window.top`). The boilerplate ships with this wired up.

## Presenter Timer & Schedule Tracking

The presenter frame supports per-deck time budgeting so the speaker can see at a glance whether they're ahead or behind schedule. This lives entirely in `presenter.html` — individual decks need no changes.

### File-level metadata

Each PLAYLIST entry takes a `minutes` field (file-level, not per-slide):

```js
const PLAYLIST = [
  { src: '00-opening.html',   label: 'Opening',      minutes: 1  },
  { src: '01-what-i-saw.html',label: 'What I Saw',   minutes: 6  },
  { src: '02-what-i-found.html',label:'What I Found',minutes: 11 },
  // ...
];
```

Time budgets should match the talk's outline doc (e.g. an `outline.md` "structure summary" table). When the user asks to allocate timings, read the outline first and sum the section budgets per deck — don't guess.

### UI elements

**Top-right wall clock** (in `.top-right` next to theme toggle):
- Shows `HH:MM` updated every tick
- Small status dot — grey when stopped, green (with glow) when running
- **Click** = start/pause the talk timer
- **Double-click** = reset all deck timers (with confirm)

**Bottom bar timer block** (in `.bottom-bar` between nav-info and nav-hints):
- `Slide  M:SS / M:SS` — elapsed vs budget for the *current* deck (cumulative across revisits — does NOT reset when you navigate back to it)
- Slim progress bar — green → amber at 80% → orange when over budget
- `Total  M:SS / M:SS` — total wall time spoken across all decks vs full talk budget
- Schedule delta pill — `±M:SS`. Green "ahead" / orange "behind".
  - `expected = sum(budgets[0..currentDeck-1]) + min(spent_current, budget_current)`
  - `delta = totalSpent - expected`
  - Backtrack-aware: uses `totalSpent` across all decks, so jumping back to an earlier deck still reflects time blown on later ones. Capping `spent_current` at the deck budget prevents the pill from flickering "behind" while you're still legitimately within the current deck's allowance.

### How time accumulates

- A `deckSpent[]` array stores cumulative seconds per deck.
- A 500ms `setInterval` calls `accumulate()` then `render()`. Accumulation only happens when `timerRunning` is true.
- When the user switches decks while the timer is running, time is "banked" onto the leaving deck before retargeting `activeDeck` to the new one. This is done by wrapping the original `switchDeck()` function — the wrapped version calls `accumulate()` first, then delegates.
- Switching decks while *paused* doesn't bank anything (`lastTick === null`).

### Implementation notes

- The timer is purely client-side, no localStorage persistence — a page refresh resets state. This is intentional: presenters typically open fresh for the talk.
- Keep the timer block CSS variables themed (uses `--green`, `--orange`, `--orange-dim`, `--ghost`) so it works in both dark and light modes.
- The status dot uses `box-shadow: 0 0 6px var(--green)` for a subtle glow when running — deliberately not flashy.
- Reference implementation: `resources/presenter-template.html` (search for "CLOCK + PER-DECK TIMER + SCHEDULE DELTA").

### When porting to other presentations

Nothing to port — `resources/presenter-template.html` already includes the timer. Instantiate the template and give each PLAYLIST entry a `minutes` value, then check the total matches the talk's target duration.
