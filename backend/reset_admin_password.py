from app.core.database import SessionLocal
from app.models.user import User
from app.core.security import hash_password

db = SessionLocal()

admin = db.query(User).filter(User.email == "admin@gmail.com").first()

if admin:
    admin.password_hash = hash_password("admin1234")
    db.commit()
    print("Admin password reset successfully")
else:
    print("Admin user not found")

db.close()