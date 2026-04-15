from flask import Flask, request, jsonify
from flask_migrate import Migrate
from datetime import date
from sqlalchemy.exc import IntegrityError
from marshmallow import ValidationError

from config import Config
from models import db, Workout, Exercise, WorkoutExercise
from schemas import *

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
migrate = Migrate(app, db)


@app.route("/")
def home():
    return {"message": "Workout API running"}


# ---------------- WORKOUTS ----------------
@app.route("/workouts", methods=["GET"])
def get_workouts():
    return jsonify(workouts_schema.dump(Workout.query.all()))


@app.route("/workouts", methods=["POST"])
def create_workout():
    try:
        data = workout_schema.load(request.json)
        workout = Workout(**data)
        db.session.add(workout)
        db.session.commit()
        return workout_schema.dump(workout), 201
    except ValidationError as e:
        return {"error": e.messages}, 400
    except ValueError as e:
        return {"error": str(e)}, 400


# ---------------- EXERCISES ----------------
@app.route("/exercises", methods=["GET"])
def get_exercises():
    return jsonify(exercises_schema.dump(Exercise.query.all()))


@app.route("/exercises", methods=["POST"])
def create_exercise():
    try:
        data = exercise_schema.load(request.json)
        exercise = Exercise(**data)
        db.session.add(exercise)
        db.session.commit()
        return exercise_schema.dump(exercise), 201
    except IntegrityError:
        db.session.rollback()
        return {"error": "Exercise must be unique"}, 400
    except ValidationError as e:
        return {"error": e.messages}, 400


# ---------------- JOIN TABLE ----------------
@app.route("/workouts/<int:w_id>/exercises/<int:e_id>", methods=["POST"])
def add_exercise(w_id, e_id):
    try:
        data = workout_exercise_schema.load(request.json)

        we = WorkoutExercise(
            workout_id=w_id,
            exercise_id=e_id,
            reps=data.get("reps"),
            sets=data.get("sets"),
            duration_seconds=data.get("duration_seconds")
        )

        db.session.add(we)
        db.session.commit()
        return {"message": "Exercise added"}, 201

    except ValidationError as e:
        return {"error": e.messages}, 400


if __name__ == "__main__":
    app.run(debug=True, port=5555)