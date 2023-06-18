from flask import Flask, render_template, url_for, jsonify, request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from forms import Search, Add, Update
import random

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap(app)

# Connect to database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy()
db.init_app(app)

class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    map_url = db.Column(db.String(250), nullable=False)
    img_url = db.Column(db.String(250), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    seats = db.Column(db.String(250), nullable=False)
    has_toilet = db.Column(db.Boolean, nullable=False)
    has_sockets = db.Column(db.Boolean, nullable=False)
    has_wifi = db.Column(db.Boolean, nullable=False)
    can_take_calls = db.Column(db.Boolean, nullable=False)
    coffee_price = db.Column(db.String(250), nullable = False)

    def __repr__(self):
        return f"< Cafe {self.name}>"
    
with app.app_context():
    # create db
    db.create_all()
    # new_cafe = Cafe(name="akk",
    #                 map_url="www.abhi.com",
    #                 image_url="www.gmail.com",
    #                 seats=50,
    #                 has_toilets=True,
    #                 has_wifi=True,
    #                 has_sockets=True,
    #                 can_take_calls=True,
    #                 coffee_price= 5)
    # db.session.add(new_cafe)
    # db.session.commit()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/cafes')
def cafes():
    all_cafes = db.session.query(Cafe).all()
    return render_template('cafes.html', cafes=all_cafes)

@app.route('/random')
def get_random_cafe():
    all_cafes = db.session.query(Cafe).all()
    random_cafe = random.choice(all_cafes)
    return render_template('cafes.html', cafes=[random_cafe])

@app.route('/search', methods=['GET', 'POST'])
def search():
    form = Search()
    if form.validate_on_submit():
        location = form.location.data.title()
        searched_cafes = db.session.query(Cafe).filter(Cafe.location == location)
        return render_template('search.html', form=form, cafes=searched_cafes)
    return render_template('search.html', form=form)

@app.route('/add', methods=['GET', 'POST'])
def add_cafe():
    form = Add()
    if form.validate_on_submit():
        name = form.name.data
        map_url = form.map_url.data
        img_url = form.img_url.data
        location = form.location.data
        has_toilet = bool(1 if form.has_toilet.data == '✅' else 0)
        has_sockets = bool(1 if form.has_sockets.data == '✅' else 0)
        has_wifi = bool(1 if form.has_wifi.data == '✅' else 0)
        can_take_calls = bool(1 if form.can_take_calls.data == '✅' else 0)
        seats = form.seats.data
        price = form.price.data
        new_cafe = Cafe(
            name=name,
            map_url=map_url,
            img_url=img_url,
            location=location,
            seats=seats,
            has_toilet=has_toilet,
            has_sockets=has_sockets,
            has_wifi=has_wifi,
            can_take_calls=can_take_calls,
            coffee_price=price
        )
        db.session.add(new_cafe)
        db.session.commit()
        return redirect(url_for('cafes'))

    return render_template('add.html', form=form)

@app.route('/update', methods=['POST', 'GET', 'PATCH'])
def update():
    cafe_id = request.args.get('id')
    selected_cafes = Cafe.query.get(cafe_id)
    form = Update(
        seats = selected_cafes.seats,
        coffee_price = selected_cafes.coffee_price
    )
    if form.validate_on_submit():
        has_sockets = bool(1 if form.has_sockets.data == '✅' else 0)
        has_toilet = bool(1 if form.has_toilet.data ==  '✅' else 0)
        has_wifi = bool(1 if form.has_wifi.data == '✅' else 0)
        can_take_calls = bool(1 if form.can_take_calls == '✅' else 0)
        seats = form.seats.data
        coffee_price = form.coffee_price.data
        selected_cafes.has_sockets = has_sockets
        selected_cafes.has_toilet = has_toilet
        selected_cafes.has_wifi = has_wifi
        selected_cafes.can_take_call = can_take_calls
        selected_cafes.seats = seats
        selected_cafes.coffee_price = coffee_price

        db.session.commit()
        return redirect(url_for('cafes'))
    return render_template('update.html', form=form)

@app.route('/delete', methods=['GET', 'POST'])
def delete():
    cafe_id = request.args.get('id')
    selected_cafe = Cafe.query.get(cafe_id)
    db.session.delete(selected_cafe)
    db.session.commit()
    return redirect(url_for('cafes'))



if __name__ == '__main__':
    app.run(debug=True)
