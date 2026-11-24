# Call Coach — working notes

The whole app is `index.html` (one self-contained page). GitHub Pages serves `main` at https://chrisurena44-eng.github.io/call-coach/ — every push to `main` goes live in about a minute.

## Release checklist
1. Edit `index.html`.
2. Bump `const APP_VERSION='N'` (open copies of the app show a "new version is ready" bar when this number goes up).
3. Add an entry at the top of `CHANGELOG.md`.
4. Run the tests:
   - `node tests/regex_test.js index.html` — objection/caution detection against sample lines (all must pass).
   - `python3 tests/ui_test.py` — demo call, practice, summary, settings in headless Chrome (only Google Fonts network errors are acceptable).
   - `python3 tests/learn_test.py` — transcript upload (TXT/DOCX/SRT), teaching, saved replies, export, reload persistence.
5. Commit and push to `main`.

## Where things live in index.html
- First `<script>`: the playbook data — `PLAYBOOK` (objections), `SIGNALS`, `CAUTIONS` (agent risk phrases), `NUDGES`, `CHECK` (discovery), `DEMO`, `KEYTERMS`. Patterns run against lower-cased text with punctuation stripped (`norm`).
- Second `<script>`: the app — live listening (Chrome speech engine or Deepgram), cue card, transcript, learning from RingCentral transcripts (`L` in localStorage `callcoach.learned`), Claude coach, summary, settings (`callcoach.cfg`).

## Context
- Built for a commercial P&C agent calling from the RingCentral web app (app.ringcentral.com) in Chrome. RingCentral's AI announcement is the default call disclosure.
- Never put API keys, transcripts or client data in this repository.
- Talk tracks must not promise coverage, claim payment or price, or encourage misstating application facts.
