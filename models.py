from app import db

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    code = db.Column(db.String(20))

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item = db.Column(db.String(100))
    amount = db.Column(db.Float)
    time = db.Column(db.DateTime)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'))
