from app import app
from app.models import db

if __name__ == "__main__":
    db.init_app(app)
    app.run(debug=True)


print("Running wsgi.py as uwsgi")