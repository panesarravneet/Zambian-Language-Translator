from flask import Flask, render_template, request, jsonify, redirect, Response, flash, url_for
from backend import ROUTE_WHITELIST, ZAM_LANGS
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.secret_key = "panesar"
# Configure database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///lingo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize DB
db = SQLAlchemy(app)

# ---------- Language-specific models ----------
class LoziContribution(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    source_text = db.Column(db.Text, nullable=False)
    english_translation = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

class TongaContribution(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    source_text = db.Column(db.Text, nullable=False)
    english_translation = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

class KaondeContribution(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    source_text = db.Column(db.Text, nullable=False)
    english_translation = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

class LundaContribution(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    source_text = db.Column(db.Text, nullable=False)
    english_translation = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

class LuvaleContribution(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    source_text = db.Column(db.Text, nullable=False)
    english_translation = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

# Model lookup based on language
language_models = {
    "lozi": LoziContribution,
    "tonga": TongaContribution,
    "kaonde": KaondeContribution,
    "lunda": LundaContribution,
    "luvale": LuvaleContribution
}

@app.route("/")
def home():
    return render_template("index.html",
                           zam_langs=ZAM_LANGS,
                           default_from="en",
                           default_to="bem")  

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

@app.route("/about")
def about():
    return render_template("about.html")

# Contribute page
@app.route("/contribute", methods=["GET", "POST"])
def contribute():
    if request.method == "POST":
        lang = request.form["language"]
        src = request.form["source"]
        eng = request.form["english"]

        # Get the correct model based on language
        model_map = {
            "lozi": LoziContribution,
            "tonga": TongaContribution,
            "kaonde": KaondeContribution,
            "lunda": LundaContribution,
            "luvale": LuvaleContribution,
        }
        Model = model_map.get(lang)
        if Model:
            new_entry = Model(source_text=src, english_translation=eng)
            db.session.add(new_entry)
            db.session.commit()
            flash("✅ Contribution submitted successfully!", "success")
        else:
            flash("⚠️ Unsupported language selection.", "error")

        return redirect(url_for("contribute"))

    return render_template("contribute.html")

@app.route("/view/<language>")
def view_contributions(language):
    language_models = {
        "lozi": LoziContribution,
        "tonga": TongaContribution,
        "kaonde": KaondeContribution,
        "lunda": LundaContribution,
        "luvale": LuvaleContribution
    }

    model = language_models.get(language.lower())
    if not model:
        return f"❌ Unsupported language: {language}", 404

    entries = model.query.order_by(model.timestamp.desc()).all()
    return render_template("view_entries.html", entries=entries, language=language.capitalize())

@app.route("/download/<language>")
def download_csv(language):
    language_models = {
        "lozi": LoziContribution,
        "tonga": TongaContribution,
        "kaonde": KaondeContribution,
        "lunda": LundaContribution,
        "luvale": LuvaleContribution
    }

    model = language_models.get(language.lower())
    if not model:
        return f"❌ Unsupported language: {language}", 404

    entries = model.query.order_by(model.timestamp.desc()).all()

    def generate():
        yield "ID,Original Text,English Translation,Timestamp\n"
        for e in entries:
            yield f"{e.id},\"{e.source_text}\",\"{e.english_translation}\",{e.timestamp}\n"

    return Response(generate(), mimetype="text/csv",
                    headers={"Content-Disposition": f"attachment;filename={language}_contributions.csv"})

@app.post("/delete/<language>")
def delete_entries(language):
    language_models = {
        "lozi": LoziContribution,
        "tonga": TongaContribution,
        "kaonde": KaondeContribution,
        "lunda": LundaContribution,
        "luvale": LuvaleContribution
    }

    model = language_models.get(language.lower())
    if not model:
        return f"❌ Unsupported language: {language}", 404

    action = request.form.get("action")
    if action == "delete":
        ids = request.form.getlist("delete_ids")
        if ids:
            model.query.filter(model.id.in_(ids)).delete(synchronize_session=False)
            db.session.commit()
    elif action == "clear":
        model.query.delete()
        db.session.commit()

    return redirect(f"/view/{language.lower()}")

if __name__ == "__main__":
    # threaded=True lets multiple requests share the single model instance
    app.run(host="0.0.0.0", port=5000, debug=True, threaded=True)
