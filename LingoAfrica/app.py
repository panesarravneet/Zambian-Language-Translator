from flask import Flask, render_template, request, jsonify
from backend import ROUTE_WHITELIST, ZAM_LANGS

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html",
                           zam_langs=ZAM_LANGS,
                           default_from="en",
                           default_to="bem")   # tweak if desired

@app.post("/translate")
def translate():
    data = request.get_json(force=True)
    route = data.get("route", "")
    text  = data.get("text", "").strip()

    # Quick sanity checks
    if not text:
        return jsonify({"error": "empty text"}), 400
    if route not in ROUTE_WHITELIST:
        return jsonify({"error": "pair not allowed"}), 400

    try:
        translation = ROUTE_WHITELIST[route](text)
    except Exception as exc:
        return jsonify({"error": str(exc)}), 500

    return jsonify({"translation": translation})

if __name__ == "__main__":
    # threaded=True lets multiple requests share the single model instance
    app.run(host="0.0.0.0", port=5000, debug=True, threaded=True)
