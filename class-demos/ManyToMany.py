# Example of many-to-many-relationships using joining tables (order-items)

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Oll1N00sh1n@localhost:5432/example'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)
order_items = db.Table('order_items', 
    db.Column('order_id', db.Integer, db.ForeignKey('order.id'), primary_key=True), 
    db.Column('product.id', db.Integer, db.ForeignKey('product.id'), primary_key=True)
)

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(), nullable=False)
    products = db.relationship('Product', secondary=order_items, backref=db.backref('orders, lazy=True'))

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)

#console/python:
#> from ManyToMany import app, db, Order, Product
#> with app.app_context(): db.create_all()
#> order=Order(status='ready')
#> product=Product(name='Great widget') 
#> order.products = [product]
#> product.orders = [order]  
#> with app.app_context(): db.session.add(order)
#> with app.app_context(): db.session.commit()    