import os
basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
#still not sure what this does
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')


#will  have to change/sort these out later
WTF_CSRF_ENABLED = True
SECRET_KEY = 'you-will-never-guess'