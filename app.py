from flask import Flask, redirect, jsonify

app = Flask(__name__)
LIVE_APP = "https://mnemos-memory-coach.heyboernathan.workers.dev/"

@app.get("/")
def home():
    return redirect(LIVE_APP, code=302)

@app.get("/api/health")
def health():
    return jsonify(ok=True, service="mini-link-studio-redirect")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
