import os # env variables

class Config:
    # Database configuration
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'postgresql://dbitems_user:dbitems_password@localhost:5432/dbitems')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
