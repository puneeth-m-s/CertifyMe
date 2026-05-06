import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from app import create_app, db

app = create_app()

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)