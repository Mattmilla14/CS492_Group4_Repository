# sync_usernames.py
# One-time fixer: set username=email where username is NULL/empty,
# so login that expects 'username' will also accept an email.
from app import app
from models import db, User

updated = 0
with app.app_context():
    users = User.query.all()
    for u in users:
        if not u.username or not u.username.strip():
            u.username = u.email
            updated += 1
    if updated:
        db.session.commit()
    print(f"Updated usernames for {updated} user(s).")