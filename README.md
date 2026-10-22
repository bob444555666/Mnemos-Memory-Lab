# MNEMOS — Memory Training Lab

A futuristic memory-training website with three playable drills, XP, levels, streaks, session history, and a 14-day activity heatmap.

## Live Cloudflare app
The production site runs as a Cloudflare Worker and stores progress in Cloudflare D1. The Worker implementation is `worker.js`; `wrangler.toml` binds the database as `DB`. Cloudflare Workers Builds is connected to the `main` branch of this repository and watches `worker.js`, `wrangler.toml`, and `package.json` for deployment changes.

## Features
- Visual Snapshot, Color Sequence, and Word Recall drills
- Daily and best streaks, XP, levels, session counts, and best score
- 14-day activity heatmap
- D1-backed server persistence
- Responsive neon game-inspired interface
- `GET /api/health`
- `GET /api/progress?player=guest-player`
- `POST /api/session` with JSON: `{"player":"guest-player","mode":"visual","score":85,"xp":30}`
- `DELETE /api/progress?player=guest-player`

## Local Python version
The Flask version in `app.py` remains available for local development:

```bash
python -m venv .venv
# Windows: .venv\\Scripts\\activate
# macOS/Linux:
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

Then open http://localhost:8000.

## Important note
The browser-generated player key is an anonymous device identifier, not a full login system. Clearing browser data or switching browsers can make a new profile. Do not use it for sensitive personal data without adding authentication and abuse protections.
