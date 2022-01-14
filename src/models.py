import db
import datetime
from sqlalchemy import Column, Integer, String, Float, ForeignKey, Table, DateTime
from sqlalchemy.orm import relationship
from flask_migrate import Migrate
from flask import Flask
from sqlalchemy.dialects.postgresql import JSONB

app = Flask(__name__)

class Role(db.Base):
    __tablename__ = 'role'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    code = Column(String, nullable=False)

class Partner(db.Base):
    __tablename__ = 'partner'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, nullable=True)
    username = Column(String, nullable=False)
    password = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    role_id = Column(Integer, ForeignKey('role.id'))
    
class Product(db.Base):
    __tablename__ = 'product'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    code = Column(String, nullable=False)
    price = Column(Float, nullable=True)

class Square(db.Base):
    __tablename__ = 'square'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=True)
    code = Column(String, nullable=True)

class Store(db.Base):
    __tablename__ = 'store'
    id = Column(Integer, primary_key=True)
    number = Column(Integer, nullable=True)
    code = Column(String, nullable=True)
    square_id = Column(Integer, ForeignKey('square.id'))

class Place(db.Base):
    __tablename__ = 'place'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=True)
    partner_id = Column(Integer, ForeignKey('partner.id'))
    product_id = Column(Integer, ForeignKey('product.id'))
    product_two_id = Column(Integer, ForeignKey('product.id'))
    product_three_id = Column(Integer, ForeignKey('product.id'))
    latitude = Column(String, nullable=True)
    longitude = Column(String, nullable=True)
    store_id = Column(Integer, ForeignKey('store.id'))
    geolocation = Column(JSONB, nullable=True )

class Udm(db.Base):
    __tablename__ = 'udm'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=True)

class ProductQualificationOffer(db.Base):
    __tablename__ = 'product_qualification_offer'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=True)
    qualification = Column(Integer)

class Post(db.Base):
    __tablename__ = 'post'
    id = Column(Integer, primary_key=True)
    post = Column(String, nullable=True)
    date_added = Column(String, nullable=True)
    place_id = Column(Integer, ForeignKey('place.id'))
    product_id = Column(Integer, ForeignKey('product.id'))
    price = Column(Float, nullable=True)
    cut_date_added = Column(String, nullable=True)
    udm_name = Column(String, nullable=True)
    product_qualification_name = Column(String, nullable=True)
    place_name = Column(String, nullable=True)
    place_latitude = Column(String, nullable=True)
    place_longitude = Column(String, nullable=True)
    product_name = Column(String, nullable=True)
    udm_id = Column(Integer, ForeignKey('udm.id'))
    product_qualification_id =  Column(Integer, ForeignKey('product_qualification_offer.id'))

 
    """def __init__(self, nombre, precio):
        self.nombre = nombre
        self.precio = precio
    def __repr__(self):
        return f'Producto({self.nombre}, {self.precio})'
    def __str__(self):
        return self.nombre"""

#serialize an object in flask
"""@property
    def serialize(self):
       Return object data in easily serializable format
       return {
           'id'         : self.id,
           'modified_at': dump_datetime(self.modified_at),
           # This is an example how to deal with Many2Many relations
           'many2many'  : self.serialize_many2many
       }"""