from flask.cli import FlaskGroup
from app import app
from app.models import db, User

cli = FlaskGroup(app)

#Creates flask cli command that Resets Database
@cli.command("recreate_db")
def recreate_db() -> None:
	db.drop_all()
	db.create_all()
	db.session.commit()
	print('[FLASK-CLI: recreate_db] CURRENT TABLES:\n',db.Model.metadata.tables.keys())

#Creates flask cli command that inserts test user to the database
@cli.command("add_test_data")
def add_test_data() -> None:
	user = User(username='test')
	user.set_password('test')

	user2 = User(username='test2')
	user2.set_password('test2')

	db.session.add(user)
	db.session.add(user2)
	db.session.commit()
	print('[FLASK-CLI: add_test_data] CURRENT USERS_TABLE STATE:\n',User.query.all())


if __name__ == "__main__":
	cli()
