# Call Coach

A live coach for commercial P&C insurance sales calls on RingCentral. While you're on a call, it listens, transcribes, and pops up what to say when a prospect raises an objection. It also flags risky things you say, tracks discovery, and learns from your RingCentral AI transcripts.

**Live app:** https://chrisurena44-eng.github.io/call-coach/

## Using it

1. Open the live app in Google Chrome, in its own window next to app.ringcentral.com.
2. Wear a headset.
3. Click **Start listening**, pick the RingCentral tab, and turn on **Also share tab audio**.
4. Read the big card when an objection comes up: **Say**, **Ask**, **Avoid**, and what you said on real calls.
5. After the call, click **End & summarize** and copy the notes.

Click **Run demo call** to see it work without a real call.

## Learning from real calls

Click **Learn from calls** and upload transcripts downloaded from RingCentral AI (TXT, DOCX, SRT or VTT, or paste the text). Save your real replies to the playbook and teach it phrases it missed. Learned data stays in your browser. Use **Export playbook** to back it up or share it.

## Updates

Changes are pushed to this repository and go live at the address above within a minute or two. An open copy of the app shows a "new version is ready" bar; reload when you're between calls. See [CHANGELOG.md](CHANGELOG.md).

## Privacy

No API keys, transcripts or learned data are stored in this repository. Keys you enter in Settings and anything the app learns are kept only in your own browser. Live audio is transcribed by Chrome's speech service, or by Deepgram if you add a Deepgram key.
