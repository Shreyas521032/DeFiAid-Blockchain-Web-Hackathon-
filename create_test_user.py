from main import app, db
from models import User
from werkzeug.security import generate_password_hash

def create_test_user():
    with app.app_context():
        test_user = User.query.filter_by(username='testuser').first()
        if not test_user:
            test_user = User(username='testuser', password_hash=generate_password_hash('testpassword'))
            db.session.add(test_user)
            db.session.commit()
            print("Test user created successfully.")
        else:
            print("Test user already exists.")

if __name__ == '__main__':
    create_test_user()
