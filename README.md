# MNEMOS — Memory Training Lab

A futuristic, game-inspired memory training website powered by Python Flask and SQLite.

## Included
- Three drills: visual snapshot, color sequence, and word recall
- Daily and best streaks, XP, levels, session counts, best score
- 14-day activity heatmap
- Python JSON API and server-side SQLite persistence
- Responsive neon HUD interface

## Run locally
Python 3.10+ is recommended.

```bash
python -m venv .venv
# Windows: .venv\\Scripts\\activate
# macOS/Linux:
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```
Then open http://localhost:8000.

## API
- `GET /api/health`
- `GET /api/progress?player=guest-player`
- `POST /api/session` with JSON: `{"player":"guest-player","mode":"visual","score":85,"xp":30}`
- `DELETE /api/progress?player=guest-player`

## Deployment
Deploy as a Python web service with the included Procfile. Set `DATABASE_URL` to a persistent database in production; the default SQLite database is intended for local use and persistent disks. This starter uses a browser-generated player key rather than full login authentication, so do not use it for sensitive personal data without adding authentication and abuse protections.
