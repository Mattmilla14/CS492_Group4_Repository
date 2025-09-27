# print_users.py
from app import app
from models import db, User

with app.app_context():
    users = User.query.all()
    if not users:
        print("No users found.")
    else:
        for u in users:
            print(f"id={u.id} email={u.email} role={u.role}")