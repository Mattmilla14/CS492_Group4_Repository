# seed_admin.py (force email + force password)
# Ensures TARGET_EMAIL exists, role=admin, and password is set to TARGET_PASSWORD.
from app import app
from models import db, User

TARGET_EMAIL = "admin@bookstore.com"
TARGET_PASSWORD = "admin123"

with app.app_context():
    db.create_all()
    u = User.query.filter_by(email=TARGET_EMAIL).first()
    if u:
        u.role = "admin"
        u.set_password(TARGET_PASSWORD)  # force reset password
        db.session.commit()
        print(f"Ensured admin and reset password for: {TARGET_EMAIL}")
    else:
        u = User(email=TARGET_EMAIL, username="admin", role="admin")
        u.set_password(TARGET_PASSWORD)
        db.session.add(u)
        db.session.commit()
        print(f"Created admin: {TARGET_EMAIL} / {TARGET_PASSWORD}")