from server.config import app, db
from server.models import Student, Instructor
import sys

def reset_password(email, new_password, user_type='student'):
    with app.app_context():
        email = email.lower().strip()
        if user_type == 'student':
            user = Student.query.filter_by(email=email).first()
        else:
            user = Instructor.query.filter_by(email=email).first()

        if not user:
            print(f"User with email {email} and user_type {user_type} not found.")
            return

        try:
            user.set_password(new_password)
            db.session.commit()
            print(f"Password reset successful for {email} ({user_type}).")
        except AssertionError as e:
            print(f"Password reset failed: {str(e)}")

if __name__ == '__main__':
    if len(sys.argv) != 4:
        print("Usage: python reset_password.py <email> <new_password> <user_type>")
        print("Example: python reset_password.py angelica@gmail.com NewPass123 student")
    else:
        email = sys.argv[1]
        new_password = sys.argv[2]
        user_type = sys.argv[3]
        reset_password(email, new_password, user_type)
