import os
from flask import Flask,render_template
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager,Shell
from app import create_app, db
from flask_sqlalchemy import SQLAlchemy
# from app.models import Vegis

# if os.path.exists('.env'):
# 	print('Importing environment from .env...')
# 	for line in open('.env'):
# 		var = line.strip().split('=')
# 		if len(var) == 2:
# 			os.environ[var[0]] = var[1]

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app,db)

app_context = app.app_context()
app_context.push()
# db.drop_all()
db.create_all()


if __name__ == '__main__':
	app.run()

