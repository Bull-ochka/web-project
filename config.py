import os

CSRF_ENABLED = True
SECRET_KEY = 'YA_KUPIL_BOTINKI_NA_SAMOM_LUCHSHEM_RINKE'

basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
