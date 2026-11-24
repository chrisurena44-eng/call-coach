# Call Coach — working notes

The whole app is `index.html` (one self-contained page). GitHub Pages serves `main` at https://chrisurena44-eng.github.io/call-coach/ — every push to `main` goes live in about a minute.

## Release checklist
1. Edit `index.html`.
2. Bump `const APP_VERSION='N'` (open copies of the app show a "new version is ready" bar when this number goes up).
3. Add an entry at the top of `CHANGELOG.md`.
4. Run the tests:
   - `node tests/regex_test.js index.html` — objection/caution detection against sample lines (all must pass).
   - `python3 tests/ui_test.py` — demo call, practice, summary, settings in headless Chrome (only Google Fonts network errors are acceptable).
   - `python3 tests/learn_test.py` — transcript upload (TXT/DOCX/SRT/RingCentral), teaching, saved replies, export, reload persistence.
   - `python3 tests/quick_test.py` — Quick objection section: tabs, Manus passcode setup and request contents, wrong passcode, Anthropic fallback, 3 more ideas, recent list (all AI mocked).
5. Commit and push to `main`.

## Where things live in index.html
- First `<script>`: the playbook data — `PLAYBOOK` (objections), `SIGNALS`, `CAUTIONS` (agent risk phrases), `NUDGES`, `CHECK` (discovery), `DEMO`, `KEYTERMS`. Patterns run against lower-cased text with punctuation stripped (`norm`).
- Second `<script>`: the app — Quick objection section (`#quick` view; `QUICK_SYS`, `runQuick`, recent list in localStorage `callcoach.quick`), live listening (Chrome speech engine or Deepgram), cue card, transcript, learning from RingCentral transcripts (`L` in localStorage `callcoach.learned`), Claude coach, summary, settings (`callcoach.cfg`).

## Context
- Built for a commercial P&C agent calling from the RingCentral web app (app.ringcentral.com) in Chrome. RingCentral's AI announcement is the default call disclosure.
- AI calls go through `claude()`: the user's Manus AI service (`POST {mUrl}/api/complete` with `{passcode, system, user, max_tokens, temperature, model}` → `{text}`) when a passcode is saved, else the Anthropic API key. Prompts live in this repo, so prompt changes never need Manus.
- Never put API keys, passcodes, transcripts or client data in this repository.
- Be conservative with the user's Manus credits: only send Manus tasks when needed, on the cheapest setting that works.
- Talk tracks must not promise coverage, claim payment or price, or encourage misstating application facts.
- Sales style: assertive closer, short spoken lines, every set ends asking for the sale or a hard next step. Agency rule: never email/text/send quotes or written price comparisons; quotes are presented live and closed on the call (asking the prospect for their dec page, loss runs or a competitor's quote is fine).
