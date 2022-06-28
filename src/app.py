from sqlalchemy.orm import session 
from sqlalchemy.orm import Session
from sqlalchemy import select
import db
from models import *
#import request
import datetime
from datetime import datetime
from flask import Flask, render_template, jsonify, request, redirect, url_for
from flask import session as ses
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
app.secret_key = '123456'
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:123456@localhost:5432/corapoyodb"
db = SQLAlchemy(app)
migrate = Migrate(app, db)
Bootstrap(app)




@app.route("/lande")
def lande():
    print('hello hello')
    return render_template('lande.html')

@app.route("/")
def index():
    ses['username'] = ''
    ses['user'] = ''
    ses['role'] = ''
    ses['date']= ''
    ses['phone'] = ''
    ses['email'] = ''
    ses['name'] = ''
    ses['last_name'] = ''
    print('hello hello')
    return render_template('index.html')
    

@app.route("/login")
def login():
    ses['username'] = ''
    ses['user'] = ''
    ses['role'] = ''
    ses['date']= ''
    print('hello hello')
    print('here is the good place')
    return render_template('login.html', ses=ses)


@app.route("/signup_two")
def close_session():
    ses['username'] = ''
    ses['user'] = ''
    ses['role'] = ''
    ses['date']= ''
    ses['phone'] = ''
    ses['email'] = ''
    ses['name'] = ''
    ses['last_name'] = ''
    print(ses['user'])
    print(ses['role'])
    print(ses['username'])
    print(ses['date'])
    print('hello hello')
    print('here is the good place 2')
    return render_template('login.html')


#login and profile

@app.route("/profile", methods=['POST'])
def profile():
    print('for here 00000')
    form = request.form
    print('for here 111')
    statement = select(Partner).filter_by(email=form['email'], password=form['password'])
    result = session.execute(statement).scalars().all()
    ses['email'] = form['email']
    ses['password'] = form['password']
    if result:
        partner = result[0]
        ses['partner_id'] = partner.id
        ses['username'] = str(partner.username)
        ses['user'] = partner.username
        role = db.session.query(Role).get(int(partner.role_id))
        ses['role'] = role.name
        ses['phone'] = partner.phone
        ses['email'] = partner.email
        ses['name'] = partner.name
        ses['last_name'] = partner.last_name
        print(ses['username'])
        #I'm cutting from here
        #products = get_products()
        statement_two = select(Place).filter_by(partner_id=partner.id)
        places = session.execute(statement_two).scalars().all()
        print('print places')
        print(len(places))
        if len(places) < 1 and role.code == 'VEN':
            return "<SCRIPT> alert('Para continuar por favor registra un puesto'); window.location='/place';  </SCRIPT>"
        #udms = db.session.query(Udm).all()
        #product_qualification_offers = db.session.query(ProductQualificationOffer).all()
        now = datetime.now()
        date_now = now.strftime("%m/%d/%Y")
        ses['date'] = date_now
        rol = ses['role']
        #statement_three = select(Post).filter_by(cut_date_added=date_now)
        #posts = session.execute(statement_three).scalars().all()
        #lis_of_localitation = [] 
        #if posts:
            #for post in posts:
                #print('from here here here')
                #print(post.place_id)
                #place = db.session.query(Place).get(int(post.place_id))
                #print(place.latitude)
                #lis_of_localitation.append(place)
        #print(posts)
        #print(len(posts))
            #place = session.query(Place).filter(partner_id=18).first()
            #place = place_list[0]
    #print('It is passing for here')

        #partner =  Partner.query.filter((Partner.username == form['email']) & (Partner.username == form['password'])).first()
    if result:
        return render_template('profile.html', partner=partner, places=places, date_now=date_now, role=role, rol=rol)
    return "<h1> La contraseña o correo se encuentran errados, por favor revisalos. </h1>"


@app.route("/recover_password")
def recover_password():
    partner = ses['username'] 
    role = ses['role']
    phone = ses['phone']
    date = ses['date'] 
    return render_template('recover_password.html', partner=partner, role=role, phone=phone, date=date)
   



@app.route("/login_two")
def login_two():
    return profile()

# Finish login and profile
"""@app.route("/login")
def login():
    print('it is passing for the map function profile')
    role = ses['role']
    date = ses['date']
    username = ses['username']
    phone = ses['phone'] 
    email = ses['email']
    name = ses['name'] 
    last_name = ses['last_name']
    return render_template('login.html', name=name, last_name=last_name, email=email, username=username, phone=phone, role=role, date=date)"""

@app.route("/publish")
def publish():
    print('it is passing for the publish function')
    partner_id = ses['partner_id']
    username = ses['username'] 
    user = ses['user']
    #role = ses['role']
    phone = ses['phone'] 
    email= ses['email'] 
    name = ses['name'] 
    last_name = ses['last_name']
    date = ses['date']
    print(ses['partner_id'])
    print(ses['username'])
    print(ses['user'])
    #print(ses['role'])
    print(ses['phone'])
    print(ses['email'])
    print(ses['name'])
    print(ses['date'])
    password = ses['password']
    statement = select(Partner).filter_by(email=ses['email'], password=ses['password'])
    result = session.execute(statement).scalars().all()
    if result:
        partner = result[0]
        role = db.session.query(Role).get(int(partner.role_id))
        print('role role role')
        print(role.code)
        if role:
            if role.code == 'COMP':
                return close_session()
        statement_two = select(Place).filter_by(partner_id=partner.id)
        places = session.execute(statement_two).scalars().all()
        udms = db.session.query(Udm).all()
        product_qualification_offers = db.session.query(ProductQualificationOffer).all()
        statement_three = select(Post).filter_by(cut_date_added=str(ses['username']))
        posts = session.execute(statement_three).scalars().all()
        products = get_products()
        role_name = role.name
    username = ses['username']
    #role = ses['role']
    date = ses['date']
    return render_template('publish.html', role=role, date=date, username=username, places=places, udms=udms, product_qualification_offers=product_qualification_offers, posts=posts, products=products, email=email, password=password, role_name=role_name)




#Hee map stars
@app.route("/map", methods=['POST'] )
def map():
    print('it is passing for the map function')
    username = ses['username']
    role = ses['role']
    date = ses['date']
    email =  ses['email']
    password = ses['password']
    phone = ses['phone']
    print('hereeeeeeeeeeeeeeeeeeeeeeeee')
    print(email)
    print(password)
    print('the session variable')
    if request.method == 'POST':
        print('the session variable 02')
        form = request.form
        print('the session variable 002')
        latitude = form['latitude']
        print('the session variable 0002')
        longitude = form['longitude']
        print('the session variable 00002')
        post = form['post']
        print('the session variable2')
        product = form['product']
        qualification = form['product_qualification_name']
        price = form['price']
        udm = form['udm']
        place = form['place']
        place_id = form['place_id']
        if place_id:
            statement_two = select(Place).filter_by(id=place_id)
            places = session.execute(statement_two).scalars().all()
            t_place = places[0]
            statement_three = select(Partner).filter_by(id=t_place.partner_id)
            partners = session.execute(statement_three).scalars().all()
            t_partner = partners[0]
            phone = t_partner.phone
    return render_template('map.html', latitude=latitude, longitude=longitude, post=post, role=role, date=date, username=username, email=email, password=password, product=product, qualification=qualification, price=price, udm=udm, place=place, phone=phone)

#Here add routers to forms   
#Here register routes starts

@app.route("/pre_register")
def pre_register():
    print('hello hello')
    roles = get_roles()
    #json_object.append(jsonify(rol))
    #print(json_object)
    return render_template('preregister.html', roles=roles)

@app.route("/register", methods=['POST'])
def register():
    print('hello hello')
    roles = get_roles()
    places = get_places()
    if request.method == 'POST':
        form = request.form
        statement = select(Role).filter_by(code=form['role'])
        result = session.execute(statement).scalars().all()
        roles = result
        role = roles[0]
        ses['role'] = role.code
    #json_object.append(jsonify(rol))
    #print(json_object)
    return render_template('register.html', roles=roles, places=places, role=role)


@app.route("/register_two")
def register_two():
    print('hello hello')
    roles = get_roles()
    places = get_places()
    #json_object.append(jsonify(rol))
    #print(json_object)
    return render_template('register.html', roles=roles, places=places)




@app.route("/place")
def register_place():
    print('hello hello')
    partners = get_partners()
    products = get_products()
    stores = get_stores()
    print('here there is very important data')
    print(ses['email'])
    statement = select(Partner).filter_by(email=ses['email'])
    result = session.execute(statement).scalars().all()
    print(result)
    if result:
        partners = result
    if len(partners) > 1:
        return "<SCRIPT> alert('No has registrado un partner'); window.location='/pre_register';  </SCRIPT>"
    rol = ses['role']
    #json_object.append(jsonify(rol))
    #print(json_object)
    return render_template('place.html', partners=partners, products=products, stores=stores,rol=rol)




@app.route("/register/square")
def register_square():
    print('hello hello')
    if ses['username'] == '':
        return render_template('signup.html')
    rol = ses['role']
    #json_object.append(jsonify(rol))
    #print(json_object)
    return render_template('square.html', rol=rol)

@app.route("/store")
def register_store():
    print('hello hello')
    squares = get_squares()
    print(squares)
    if ses['username'] == '':
        return render_template('signup.html')
    rol = ses['role']
    #json_object.append(jsonify(rol))
    #print(json_object)
    return render_template('store.html', squares=squares, rol=rol)

@app.route("/product")
def register_product():
    print('hello hello')
    if ses['username'] == '':
        return render_template('signup.html')
    rol = ses['role']
    #json_object.append(jsonify(rol))
    #print(json_object)
    return render_template('product.html', rol=rol)




@app.route("/role")
def register_role():
    print('This is very important')
    print(ses['username'])
    if ses['username'] == '':
        return render_template('signup.html')
    rol = ses['role']
    #json_object.append(jsonify(rol))
    #print(json_object)
    return render_template('role.html', rol=rol)

@app.route("/post")
def register_post():
    print('hello hello -1')
    #json_object.append(jsonify(rol))
    #print(json_object)
    products = get_products()
    places = get_places()
    udms = db.session.query(Udm).all()
    qualifications = db.session.query(ProductQualificationOffer).all()
    if ses['role'] == "Beneficiario":
        statement_three = select(Post).filter_by(cut_date_added=str(ses['date']), donation=True)
    else:
        statement_three = select(Post).filter_by(cut_date_added=str(ses['date']), donation=False)
    posts = session.execute(statement_three).scalars().all()
    email = ses['email']
    password = ses['password']
    username = ses['username']
    date = ses['date']
    role = ses['role']
    print(ses['username'])
    print(ses['date'])
    print(ses['role'])
    partner = db.session.query(Partner).get(int(ses['partner_id']))
    #role = db.session.query(Role).get(int(partner.role_id))
    print('post post post')
    return render_template('post.html', products=products, places=places, udms=udms, qualifications=qualifications, posts=posts, email=email, password=password,role=role, username=username, date=date)

@app.route("/post_p")
def post_p():
    print('hello hello 0')
    #json_object.append(jsonify(rol))
    #print(json_object)
    products = get_products()
    places = get_places()
    udms = db.session.query(Udm).all()
    qualifications = db.session.query(ProductQualificationOffer).all()
    statement_three = select(Post).order_by(Post.price).filter_by(cut_date_added=str(ses['date']))
    posts = session.execute(statement_three).scalars().all()
    if posts:
        list_posts = []
        for post in posts[::-1]:
            list_posts.append(post)
        posts = list_posts
    print('this is first type')
    print(type(posts))
    #posts = statement_three.order_by('price')
    print('this is second type')
    print(type(posts))
    email = ses['email']
    password = ses['password']
    print(type(posts))
    print('this is test to Charlie')
    username = ses['username']
    date = ses['date']
    role = ses['role']
    print(ses['username'])
    print(ses['date'])
    print(ses['role'])
    partner = db.session.query(Partner).get(int(ses['partner_id']))
    #role = db.session.query(Role).get(int(partner.role_id))
    print('post post post')
    return render_template('post.html', products=products, places=places, udms=udms, qualifications=qualifications, posts=posts, email=email, password=password,role=role, username=username, date=date)


@app.route("/post_pmy")
def post_pmy():
    print('hello hello 1')
    #json_object.append(jsonify(rol))
    #print(json_object)
    products = get_products()
    places = get_places()
    udms = db.session.query(Udm).all()
    qualifications = db.session.query(ProductQualificationOffer).all()
    statement_three = select(Post).order_by(Post.price).filter_by(cut_date_added=str(ses['date']))
    posts = session.execute(statement_three).scalars().all()
    print('this is first type')
    print(type(posts))
    #posts = statement_three.order_by('price')
    print('this is second type')
    print(type(posts))
    email = ses['email']
    password = ses['password']
    print(type(posts))
    print('this is test to Charlie')
    username = ses['username']
    date = ses['date']
    role = ses['role']
    print(ses['username'])
    print(ses['date'])
    print(ses['role'])
    partner = db.session.query(Partner).get(int(ses['partner_id']))
    #role = db.session.query(Role).get(int(partner.role_id))
    print('post post post')
    return render_template('post.html', products=products, places=places, udms=udms, qualifications=qualifications, posts=posts, email=email, password=password,role=role, username=username, date=date)

@app.route("/post_name", methods=['POST'])
def post_name():
    print('hello hello')
    #json_object.append(jsonify(rol))
    #print(json_object)
    form = request.form
    products = get_products()
    places = get_places()
    udms = db.session.query(Udm).all()
    qualifications = db.session.query(ProductQualificationOffer).all()
    statement_three = select(Post).order_by(Post.price).filter_by(cut_date_added=str(ses['date']), product_name=form['product_name'])
    posts = session.execute(statement_three).scalars().all()
    print('this is first type')
    print(type(posts))
    if posts:
        list_posts = []
        for post in posts[::-1]:
            list_posts.append(post)
        posts = list_posts
    #posts = statement_three.order_by('price')
    print('this is second type')
    print(type(posts))
    email = ses['email']
    password = ses['password']
    print(type(posts))
    print('this is test to Charlie')
    username = ses['username']
    date = ses['date']
    role = ses['role']
    print(ses['username'])
    print(ses['date'])
    print(ses['role'])
    partner = db.session.query(Partner).get(int(ses['partner_id']))
    #role = db.session.query(Role).get(int(partner.role_id))
    print('post post post')
    return render_template('post.html', products=products, places=places, udms=udms, qualifications=qualifications, posts=posts, email=email, password=password,role=role, username=username, date=date)

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
        ses['eamil'] = form['email']
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
    role = get_role(form['role_id'])
    print('sementhing')
    ses['email'] = form['email']
    print(ses['email'])
    print('sementhing 1')
    print(role.name)
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
    if role.code == 'VEN':
        return "<SCRIPT> alert('Registro exitoso'); window.location='/place';  </SCRIPT>"
    else:
        return "<SCRIPT> alert('Registro exitoso'); window.location='/login';  </SCRIPT>"

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
    return role

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
    print(ses['username'])
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
    return "<SCRIPT> alert('Registro exitoso'); window.location='/login';  </SCRIPT>"

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
        print('it is passing for here')
        now = datetime.now()
        date_now = now.strftime("%m/%d/%Y, %H:%M:%S")
        date_now_cut = now.strftime("%m/%d/%Y")
        form = request.form
        print('It is passing for here 1')
        print(form['udm_id'])
        udm_object = db.session.query(Udm).get(form['udm_id'])
        print('It is passing for here 2')
        product_qualification_object = db.session.query(ProductQualificationOffer).get(form['product_qualification_id'])
        print('It is passing for here 3')
        place_object = db.session.query(Place).get(form['place_id'])
        print('It is passing for here 4')
        product_object = db.session.query(Product).get(form['product_id'])
        print('It is passing for here 5')
        print(form['donation'])
        print(eval(form['donation']))
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
        product_qualification_id = int(form['product_qualification_id']),
        donation = eval(form['donation'])
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
    #return "<SCRIPT> alert('Publicación exitosa'); window.location=/post;  </SCRIPT>"
    return register_post()

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
