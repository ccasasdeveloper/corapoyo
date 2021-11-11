from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, static_url_path='/static')


engine = create_engine('postgresql://postgres:123456@localhost:5432/corapoyodb')
Session = sessionmaker(bind=engine)
session = Session()
app.config['SQLALCHEMY_DATABASE_URI'] = "'postgresql://postgres:123456@localhost:5432/corapoyodb"
db = SQLAlchemy(app)
Base = declarative_base()