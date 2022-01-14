from sqlalchemy.orm import session
from sqlalchemy.orm import Session
from sqlalchemy import select
import db
from models import *
#import request
import datetime
from datetime import datetime
from flask import Flask, render_template, jsonify, request
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
import bigdatacloudapi
import json 
import requests
from sqlalchemy import create_engine


app = Flask(__name__)
engine = create_engine('postgresql://postgres:123456@localhost:5432/corapoyodb')
session = Session(engine, future=True)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:123456@localhost:5432/corapoyodb"
db = SQLAlchemy(app)
migrate = Migrate(app, db)
Bootstrap(app)




@app.route("/")
def index():
    print('hello hello')
    return render_template('index.html')
    

@app.route("/signup")
def signup():
    print('hello hello')
    return render_template('signup.html')


#login and profile

@app.route("/login", methods=['POST'])
def login():
    print('for here 00000')
    if request.method == 'POST':
        form = request.form
        print('for here 111')
        statement = select(Partner).filter_by(email=form['email'], password=form['password'])
        result = session.execute(statement).scalars().all()
        if result:
            partner = result[0]
            products = get_products()
            statement_two = select(Place).filter_by(partner_id=partner.id)
            places = session.execute(statement_two).scalars().all()
            udms = db.session.query(Udm).all()
            product_qualification_offers = db.session.query(ProductQualificationOffer).all()
            print(udms)
            print(product_qualification_offers)
            now = datetime.now()
            date_now = now.strftime("%m/%d/%Y")
            statement_three = select(Post).filter_by(cut_date_added=date_now)
            posts = session.execute(statement_three).scalars().all()
            print(posts)
            print(len(posts))
            #place = session.query(Place).filter(partner_id=18).first()
            #place = place_list[0]
        print('It is passing for here')
        #partner =  Partner.query.filter((Partner.username == form['email']) & (Partner.username == form['password'])).first()
        if result:
            return render_template('profile.html', partner=partner, places=places, products=products, udms=udms, product_qualification_offers=product_qualification_offers, posts=posts, date_now=date_now)
        return "<h1> La contraseña o correo se encuentran errados, por favor revisalos. </h1>"


# Finish login and profile
    

#Hee map stars
"""@app.route("/map")
def map():
    #answ = requests.get('https://maps.googleapis.com/maps/api/js?key=AIzaSyCzMTiovnfjwuc7imN6qCDXoEbPO4-q_XU&callback=initMap&v=weekly')
    #print(answ)
    #roles = get_roles()
    #json_object.append(jsonify(rol))
    #print(json_object)
    return render_template('map.html')"""

#Here add routers to forms   
#Here register routes starts

@app.route("/register")
def register():
    print('hello hello')
    roles = get_roles()
    #json_object.append(jsonify(rol))
    #print(json_object)
    return render_template('register.html', roles=roles)

@app.route("/place")
def register_place():
    print('hello hello')
    partners = get_partners()
    products = get_products()
    stores = get_stores()
    #json_object.append(jsonify(rol))
    #print(json_object)
    return render_template('place.html', partners=partners, products=products, stores=stores)

@app.route("/register/square")
def register_square():
    print('hello hello')
    #json_object.append(jsonify(rol))
    #print(json_object)
    return render_template('square.html')

@app.route("/store")
def register_store():
    print('hello hello')
    squares = get_squares()
    print(squares)
    #json_object.append(jsonify(rol))
    #print(json_object)
    return render_template('store.html', squares=squares)

@app.route("/product")
def register_product():
    print('hello hello')
    #json_object.append(jsonify(rol))
    #print(json_object)
    return render_template('product.html')

@app.route("/role")
def register_role():
    print('hello hello')
    #json_object.append(jsonify(rol))
    #print(json_object)
    return render_template('role.html')

@app.route("/post")
def register_post():
    print('hello hello')
    #json_object.append(jsonify(rol))
    #print(json_object)
    products = get_products()
    places = get_places()
    return render_template('post.html', products=products, places=places)


#Here register finished

#Here partner stars

@app.route("/partners", methods=['GET'])
def get_partners():
    partners = db.session.query(Partner).all()
    print(partners)
    print(type(partners))
    if partners:
        return partners
    return

@app.route("/partner", methods=['POST'])
def create_partner():
    print('for here 0')
    if request.method == 'POST':
        print('for here 01')
        form = request.form
        print(form)
        print('for here 02')
        partner = Partner(
        name=str(form['name']),
        last_name=str(form['last_name']), 
        email=str(form['email']), 
        username=str(form['username']), 
        password=str(form['password']), 
        phone=str(form['phone']), 
        role_id=int(form['role_id'])
    )
    print('for here 2')
    db.session.add(partner)
    db.session.commit()
    print(partner.id)
    """partner = Partner(
        name=str(request.json['name']),
        last_name=str(request.json['last_name']), 
        email=str(request.json['email']), 
        username=str(request.json['username']), 
        password=str(request.json['password']), 
        phone=int(request.json['phone']), 
        role_id=int(request.json['role_id'])
    )
    db.session.add(partner)
    db.session.commit()
    print(partner.id)"""
    return "<p> Succesfully </p>"

@app.route("/partner/<id>", methods=['GET'])
def get_partner(id):
    partner = db.session.query(Partner).get(
        int(id)
    )
    print(partner.id)
    print(partner.name)
    return "<p>Hello, World!</p>"

@app.route("/partner/<id>", methods=['POST'])
def delete_partner(id):
    partner = db.session.query(Partner).get(
        int(id)
    )
    print(partner.id)
    print(partner.name)
    db.session.delete(partner)
    return "<p>Hello, World!</p>"

@app.route("/partner/<id>", methods=['PUT'])
def update_partner(id):
    partner = db.session.query(Partner).get(
        int(id)
    )
    print(partner.id)
    print(partner.name)
    return "<p>Hello, World!</p>"

# Here partner finished
# here role starts

@app.route("/roles", methods=['GET']) 
def get_roles():
    roles = db.session.query(Role).all()
    print(roles)
    print(type(roles))
    if roles:
        return roles
    return

@app.route("/role", methods=['POST'])
def create_role():
    if request.method == 'POST':
        form = request.form
        print('for here 02')
        role = Role(
        name=str(form['name']),
        code=str(form['code'])
        
    )
    print('for here 2')
    db.session.add(role)
    db.session.commit()
    print('for here 3')
    print(role.id)
    """role = Role(
        name=str(request.json['name']),
        code=str(request.json['code']),
    )
    db.session.add(role)
    db.session.commit()
    print(role.id)"""
    return "<p> Succesfully </p>"

@app.route("/role/<id>", methods=['GET'])
def get_role(id):
    role = db.session.query(Role).get(
        int(id)
    )
    print(role.id)
    print(role.name)
    return "<p>Hello, World!</p>"

@app.route("/role/<id>", methods=['DELETE'])
def delete_role(id):
    role = db.session.query(Role).get(
        int(id)
    )
    db.session.delete(role)
    return "<p>Hello, World!</p>"

@app.route("/role/<id>", methods=['PUT'])
def update_role(id):
    role = db.session.query(Role).get(
        int(id)
    )
    print(role.id)
    return "<p>Hello, World!</p>"

# Here role finished
# Here product stars

@app.route("/products", methods=['GET'])
def get_products():
    products = db.session.query(Product).all()
    if products:
        return products
    return

@app.route("/product", methods=['POST'])
def create_product():
    if request.method == 'POST':
        form = request.form
        product = Product(
        name=str(form['name']),
        code=str(form['code']),
        price=float(form['price'])
    )
    print('for here 2')
    db.session.add(product)
    db.session.commit()
    print('for here 3')
    print(product.id)
    """product = Product(
        name=str(request.json['name']),
        code=str(request.json['code']),
        price=str(request.json['price']),
    )
    db.session.add(product)
    db.session.commit()
    print(product.id)"""
    return "<p> Succesfully </p>"

@app.route("/product/<id>", methods=['GET'])
def get_product(id):
    product = db.session.query(Product).get(
        int(id)
    )
    print(product.id)
    print(product.name)
    return "<p>Hello, World!</p>"

@app.route("/product/<id>", methods=['POST'])
def delete_product(id):
    product = db.session.query(Product).get(
        int(id)
    )
    db.session.delete(product)
    return "<p>Hello, World!</p>"

@app.route("/product/<id>", methods=['PUT'])
def update_product(id):
    product = db.session.query(Product).get(
        int(id)
    )
    print(product.id)
    print(product.name)
    return "<p>Hello, World!</p>"

# Here product finished
# Here place stars

@app.route("/places", methods=['GET'])
def get_places():
    places = db.session.query(Place).all()
    print(places)
    print(type(places))
    #print(jsonify(products))
    if places:
        return places
    return

@app.route("/place", methods=['POST'])
def create_place():
    apiKey = 'd603b3d9f55c4e99b732d4cf9436dfba'
    client = bigdatacloudapi.Client(apiKey)
    resultObject,httpResponseCode = client.getIpGeolocationFull({"ip":"186.102.4.77"})
    print('HTTP Response Code: ',httpResponseCode)
    print('Lookup IP: ',resultObject['ip'])
    print('Latitude: ',resultObject['location']['latitude'])
    print('Longitude: ',resultObject['location']['longitude'])
    latitude = resultObject['location']['latitude']
    longitude = resultObject['location']['longitude']
    print(type(str(latitude)))
    print(type(str(longitude)))
    print(type(json.dumps(resultObject)))
    if request.method == 'POST':
        form = request.form
        print('yes')
        place = Place(
        name=str(form['name']),
        partner_id=int(form['partner_id']),
        product_id=int(form['product_id']),
        product_two_id=int(form['product_two_id']),
        product_three_id=int(form['product_three_id']),

        latitude = str(form['almcLati']),
        longitude = str(form['almcLong']),
        store_id=int(form['store_id']),
        #geolocation = json.dumps(resultObject)
    )
    print('hello Carlos')
    print('for here 2')
    print(place)
    db.session.add(place)
    db.session.commit()
    print('for here 3')
    print(place.id)
    """place = Place(
        store=str(request.json['store']),
        name=str(request.json['name']),
        partner_id=int(request.json['partner_id']),
        product_id=int(request.json['product_id']),
        product_two_id=int(request.json['product_two_id']),
        product_three_id=int(request.json['product_three_id'])
    )
    db.session.add(place)
    db.session.commit()
    print(place.id)"""
    return"<p> Succesfully </p>"

@app.route("/place/<id>", methods=['GET'])
def get_place(id):
    place = db.session.query(Place).get(
        int(id)
    )
    print(place.id)
    print(place.name)
    return "<p>Hello, World!</p>"

@app.route("/place/<id>", methods=['POST'])
def delete_place(id):
    place = db.session.query(Place).get(
        int(id)
    )
    print(place.id)
    print(place.name)
    db.session.delete(place)
    return "<p>Hello, World!</p>"

@app.route("/place/<id>", methods=['PUT'])
def update_place():
    place = db.session.query(Place).get(
        int(id)
    )
    print(place.id)
    print(place.name)
    return "<p>Hello, World!</p>"

# here place finished
# Here post stars

@app.route("/posts", methods=['GET'])
def get_posts():
    posts = db.session.query(Post).all()
    print(posts)
    print(type(posts))
    if posts:
        return posts
    return

@app.route("/post", methods=['POST'])
def create_post():
    if request.method == 'POST':
        now = datetime.now()
        date_now = now.strftime("%m/%d/%Y, %H:%M:%S")
        date_now_cut = now.strftime("%m/%d/%Y")
        form = request.form
        udm_object = db.session.query(Udm).get(form['udm_id'])
        product_qualification_object = db.session.query(ProductQualificationOffer).get(form['product_qualification_id'])
        place_object = db.session.query(Place).get(form['place_id'])
        product_object = db.session.query(Product).get(form['product_id'])
        post = Post(
        post=str(form['post']),
        date_added=str(date_now),
        place_id=int(form['place_id']),
        product_id=int(form['product_id']),
        price=float(form['price']),
        cut_date_added = str(date_now_cut),
        udm_name = udm_object.name,
        product_qualification_name = product_qualification_object.name,
        place_name = place_object.name,
        place_latitude = place_object.latitude,
        place_longitude =place_object.longitude,
        product_name = product_object.name,
        udm_id = int(form['udm_id']),
        product_qualification_id = int(form['product_qualification_id'])
    )
    print('for here 2')
    db.session.add(post)
    db.session.commit()
    print('for here 3')
    print(post.id)
    """partner = Partner(name='Firstusername')
    db.session.add(partner)
    db.session.commit()
    print(partner.id)"""

    return "<p> Succesfully </p>"

@app.route("/post/<id>", methods=['GET'])
def get_post():
    """partner = Partner(name='Firstusername')
    db.session.add(partner)
    db.session.commit()
    print(partner.id)"""
    return "<p>Hello, World!</p>"

@app.route("/post/<id>", methods=['POST'])
def delete_post():
    """partner = Partner(name='Firstusername')
    db.session.add(partner)
    db.session.commit()
    print(partner.id)"""
    return "<p>Hello, World!</p>"

@app.route("/post/<id>", methods=['PUT'])
def update_post():
    """partner = Partner(name='Firstusername')
    db.session.add(partner)
    db.session.commit()
    print(partner.id)"""
    return "<p>Hello, World!</p>"

# Here post finished
# Here square starts

@app.route("/squares", methods=['GET'])
def get_squares():
    squares = db.session.query(Square).all()
    print(squares)
    print(type(squares))
    if squares:
        return squares
    return



@app.route("/register/square", methods=['POST'])
def create_square():
    print('from here is passing')
    if request.method == 'POST':
        print('from here is passing 2')
        form = request.form
        print('from here is passing 3')
        square = Square(
        name=str(form['name']),
        code=str(form['code'])
        #name='hellohello',
        #code='12345' 
    )
    print('for here 2')
    db.session.add(square)
    db.session.commit()
    print('for here 3')
    print(square.id)
    return "<p> Succesfully </p>"

@app.route("/square/<id>", methods=['GET'])
def get_square():
    """partner = Partner(name='Firstusername')
    db.session.add(partner)
    db.session.commit()
    print(partner.id)"""
    return "<p>Hello, World!</p>"

@app.route("/square/<id>", methods=['POST'])
def delete_square():
    """partner = Partner(name='Firstusername')
    db.session.add(partner)
    db.session.commit()
    print(partner.id)"""
    return "<p>Hello, World!</p>"

@app.route("/post/<id>", methods=['PUT'])
def update_square():
    """partner = Partner(name='Firstusername')
    db.session.add(partner)
    db.session.commit()
    print(partner.id)"""
    return "<p>Hello, World!</p>"

# Here squares finished
# Here store stars

@app.route("/stores", methods=['GET'])
def get_stores():
    stores = db.session.query(Store).all()
    print(stores)
    print(type(stores))
    if stores:
        return stores
    return

@app.route("/store", methods=['POST'])
def create_store():
    print('from here is passing')
    if request.method == 'POST':
        print('from here is passing 2')
        form = request.form
        print('from here is passing 3')
        store = Store(
        number=int(form['number']),
        code=str(form['code']),
        square_id=int(form['square_id'])
        #name='hellohello',
        #code='12345' 
    )
    print('for here 2')
    db.session.add(store)
    db.session.commit()
    print('for here 3')
    print(store.id)
    """store = Store(
        number=int(request.json['name']),
        code=str(request.json['code']),
        square_id=int(request.json['price']),
    )
    db.session.add(store)
    db.session.commit()
    print(store.id)"""
    return "<p> Succesfully </p>"

"""def run():
    partner = Partner('Firstusername')
    db.session.add(partner)
if __name__ == '__main__':
    db.Base.metadata.create_all(db.engine)
    app.run()"""

if __name__ == '__main__':
    app.run(debug=True)