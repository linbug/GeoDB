import os
basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'postgresql://nasa:lin@localhost'
# SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')