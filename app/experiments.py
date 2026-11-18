
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.evaluation import EqualWeightStrategy


from app import db
from app.models import Experiment

experiments = Blueprint("experiments", __name__)


@experiments.route("/experiments/new", methods=["GET", "POST"])
@login_required
def new_experiment():
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        prompt = request.form.get("prompt", "").strip()
        ai_response = request.form.get("ai_response", "").strip()
        notes = request.form.get("notes", "").strip()

        try:
            relevance_score = int(request.form.get("relevance_score", ""))
            clarity_score = int(request.form.get("clarity_score", ""))
            completeness_score = int(request.form.get("completeness_score", ""))
        except ValueError:
            flash("Please provide valid scores for all three evaluation criteria.")
            return redirect(url_for("experiments.new_experiment"))

        if not title or not prompt or not ai_response:
            flash("Please complete the title, prompt, and AI response.")
            return redirect(url_for("experiments.new_experiment"))

        scores = [relevance_score, clarity_score, completeness_score]

        if any(score < 1 or score > 5 for score in scores):
            flash("Each evaluation score must be between 1 and 5.")
            return redirect(url_for("experiments.new_experiment"))

        strategy = EqualWeightStrategy()
        rating = strategy.calculate(
            relevance_score,
            clarity_score,
            completeness_score
)

        experiment = Experiment(
            title=title,
            prompt=prompt,
            ai_response=ai_response,
            relevance_score=relevance_score,
            clarity_score=clarity_score,
            completeness_score=completeness_score,
            rating=rating,
            notes=notes,
            user_id=current_user.id
        )

        db.session.add(experiment)
        db.session.commit()

        flash("Your experiment has been saved successfully!")
        return redirect(url_for("experiments.new_experiment"))

    return render_template("new_experiment.html")
