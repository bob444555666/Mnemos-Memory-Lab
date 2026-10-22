from datetime import date, datetime, timedelta
import os
from pathlib import Path
from flask import Flask, jsonify, request, render_template
from flask_sqlalchemy import SQLAlchemy

BASE = Path(__file__).resolve().parent
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL", f"sqlite:///{BASE / 'mnemos.db'}")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    player_key = db.Column(db.String(80), unique=True, nullable=False)
    xp = db.Column(db.Integer, default=0, nullable=False)
    level = db.Column(db.Integer, default=1, nullable=False)
    streak = db.Column(db.Integer, default=0, nullable=False)
    best_streak = db.Column(db.Integer, default=0, nullable=False)
    last_played = db.Column(db.Date, nullable=True)

class Session(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    player_id = db.Column(db.Integer, db.ForeignKey("player.id"), nullable=False)
    mode = db.Column(db.String(30), nullable=False)
    score = db.Column(db.Integer, nullable=False)
    xp = db.Column(db.Integer, nullable=False)
    played_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

with app.app_context():
    db.create_all()

def get_player(key):
    key = (key or "guest-player").strip()[:80] or "guest-player"
    p = Player.query.filter_by(player_key=key).first()
    if p is None:
        p = Player(player_key=key)
        db.session.add(p)
        db.session.commit()
    return p

def payload(p):
    recent = Session.query.filter_by(player_id=p.id).order_by(Session.played_at.desc()).limit(100).all()
    activity = {}
    for s in recent:
        k = s.played_at.date().isoformat()
        activity[k] = activity.get(k, 0) + 1
    today = date.today()
    return {"player": p.player_key, "xp": p.xp, "level": p.level,
            "xpToNext": 250, "currentStreak": p.streak, "bestStreak": p.best_streak,
            "lastPlayed": p.last_played.isoformat() if p.last_played else None,
            "sessions": len(recent), "bestScore": max((s.score for s in recent), default=0),
            "activity": [{"date": (today-timedelta(days=i)).isoformat(),
                          "count": activity.get((today-timedelta(days=i)).isoformat(), 0)}
                         for i in range(13, -1, -1)],
            "recent": [{"mode":s.mode,"score":s.score,"xp":s.xp,"playedAt":s.played_at.isoformat()+"Z"} for s in recent[:8]]}

@app.get("/")
def home():
    return render_template("index.html")

@app.get("/api/health")
def health():
    return jsonify(ok=True, service="mnemos-python", time=datetime.utcnow().isoformat()+"Z")

@app.get("/api/progress")
def get_progress():
    return jsonify(payload(get_player(request.args.get("player"))))

@app.post("/api/session")
def save_session():
    data = request.get_json(silent=True) or {}
    p = get_player(data.get("player"))
    score = max(0, min(100, int(data.get("score", 0))))
    xp = max(10, min(100, int(data.get("xp", 20))))
    today = date.today()
    if p.last_played != today:
        p.streak = p.streak + 1 if p.last_played == today-timedelta(days=1) else 1
        p.last_played = today
    p.best_streak = max(p.best_streak, p.streak)
    p.xp += xp
    p.level = p.xp // 250 + 1
    db.session.add(Session(player_id=p.id, mode=str(data.get("mode","visual"))[:30], score=score, xp=xp))
    db.session.commit()
    return jsonify(saved=True, progress=payload(p))

@app.delete("/api/progress")
def reset_progress():
    p = get_player(request.args.get("player"))
    Session.query.filter_by(player_id=p.id).delete()
    p.xp, p.level, p.streak, p.best_streak, p.last_played = 0, 1, 0, 0, None
    db.session.commit()
    return jsonify(reset=True)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT","8000")))
