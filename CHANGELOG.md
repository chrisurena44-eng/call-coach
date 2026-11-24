# Changelog

## v13 — Nov 23, 2026
- Phone-friendly: on a phone the site opens on Quick objection, and the live-call buttons are hidden there on small screens so the objection box sits at the top (Settings stays).
- Tapping Start listening on a phone explains that live listening needs Chrome on a computer.

## v12 — Nov 23, 2026
- Your Manus AI service address is built in, so connecting the AI only takes the passcode.

## v11 — Nov 23, 2026
- AI can now run through your own **Manus AI service** (Manus's built-in Claude), so no Anthropic API key is needed. Paste the service address and passcode in Quick objection's setup box or in Settings; they're saved only in your browser.
- All AI features use the same connection: Quick objection, the live coach, Analyze with Claude, and AI call notes. An Anthropic key still works as a fallback.
- Clear messages for a wrong passcode, the hourly limit, or an unreachable service.

## v10 — Nov 23, 2026
- API key help now points to the Claude Console at platform.claude.com/settings/keys.

## v9 — Nov 23, 2026
- **Quick objection is its own section.** Switch between **Live call** and **Quick objection** with the tabs under the header, or press / anywhere.
- Claude writes three pointers specific to the exact objection and its details: acknowledge and reframe, the question that uncovers what's behind it, and a concrete next step. A one-line read on what's likely going on comes first.
- Optional context (type of business, coverage, details) makes the pointers sharper; business type and coverage are remembered.
- **3 more ideas** asks Claude for three different pointers. **Recent objections** keeps your last 30 lookups in this browser.
- If no API key is saved, the section asks for it right there; until then it shows the matching playbook card.

## v8 — Nov 23, 2026
- Quick objection now stays on the objection you typed: it picks the single best-matching objection, shows "Matched objection", and all 3 pointers address it (acknowledge and reframe, find the real concern, set the next step or what worked before).
- Every objection and buying signal has a new next-step line.
- Claude gets only that objection's notes and your past replies to it, is told all 3 pointers must answer that exact objection, and runs at a lower temperature for focus.

## v7 — Nov 23, 2026
- **Quick objection** box at the top: type what the prospect said and press Enter for 3 pointers (what to say plus a follow-up question). Uses Claude when an Anthropic key is in Settings, grounded in your playbook, saved real replies and the live transcript; otherwise shows the closest playbook matches.
- Press / anywhere to jump to the box; Esc clears it. Typed objections appear in Earlier pointers and in the call summary.

## v6 — Nov 23, 2026
- Reads RingCentral AI transcript downloads (the `Name | Date Time` layout).
- Learned from a real call: new objection "My buddy pays less", new buying signal "wants to lock in a start date", new caution for sharing another client's price or policy details.
- New coaching moments on your own lines: "Set a time before you hang up" and "Quote expiring: ask for the bind".
- Discovery checklist adds "Bond and license requirements"; start/effective dates count toward the date item.
- Transcript review shows buying signals and coaching moments for each call.

## v5 — Nov 23, 2026
- Hosted on GitHub Pages; updates go live automatically.
- Version number in the header, and a "new version is ready" bar when an update is published.

## v4
- **Learn from calls**: upload RingCentral AI transcripts (TXT, DOCX, SRT, VTT or pasted text). Finds objections and your real replies, flags risky phrases, and lists lines the coach missed.
- Teach new phrases or new objections; saved replies show on the cue card ("Worked before" for sold calls).
- Optional Claude analysis of each transcript; export/import the learned playbook.

## v3
- RingCentral's AI announcement is the default call disclosure (consent checkbox can be turned back on in Settings).

## v2
- RingCentral setup: share picker opens on Chrome tabs; caller-audio meter.
- Playbook expanded with Manus research: 28 objection cards, 2 buying-signal types, 7 agent cautions.

## v1
- Live listening (Chrome speech engine or Deepgram), objection cards, buying signals, agent cautions, discovery checklist, talk-time nudges, optional Claude coach, end-of-call summary, demo and practice modes.
