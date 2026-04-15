from app import app
from models import db, Workout, Exercise
from datetime import date

with app.app_context():
    db.drop_all()
    db.create_all()

    e1 = Exercise(name="Push Up", category="strength", equipment_needed=False)
    e2 = Exercise(name="Run", category="cardio", equipment_needed=False)

    w1 = Workout(date=date.today(), duration_minutes=30)

    db.session.add_all([e1, e2, w1])
    db.session.commit()

    print("Database seeded")