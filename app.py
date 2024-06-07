from flask import Flask, request, jsonify, render_template, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from authlib.integrations.flask_client import OAuth
import africastalking
import datetime
import os

from dotenv import load_dotenv
load_dotenv()


app = Flask(__name__)
app.config.from_object('config.Config')
db = SQLAlchemy(app)
ma = Marshmallow(app)
oauth = OAuth(app)

# Configure OpenID Connect with your provider details
oauth.register(
    name='auth0',
    client_id=os.getenv('AUTH0_CLIENT_ID'),
    client_secret=os.getenv('AUTH0_CLIENT_SECRET'),
    server_metadata_url=f'https://{os.getenv("AUTH0_DOMAIN")}/.well-known/openid-configuration',
    client_kwargs={
        'scope': 'openid profile email',
    }
)

# Africas Talking Configuration
africastalking.initialize('username', 'api_key')
sms = africastalking.SMS

# Models
class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    code = db.Column(db.String(20))

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item = db.Column(db.String(100))
    amount = db.Column(db.Float)
    time = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'))

# Schemas
class CustomerSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Customer

class OrderSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Order

customer_schema = CustomerSchema()
customers_schema = CustomerSchema(many=True)
order_schema = OrderSchema()
orders_schema = OrderSchema(many=True)

# Routes
@app.route('/')
def index():
    return render_template('base.html')

@app.route('/login')
def login():
    return oauth.auth0.authorize_redirect(redirect_uri=url_for('callback', _external=True))

@app.route('/callback')
def callback():
    token = oauth.auth0.authorize_access_token()
    user_info = token.get('userinfo')
    session['user'] = user_info
    return redirect(url_for('profile'))

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('index'))

@app.route('/profile')
def profile():
    user = session.get('user')
    if user:
        return render_template('profile.html', user=user)
    return redirect(url_for('login'))

@app.route('/customers', methods=['GET', 'POST'])
def manage_customers():
    if request.method == 'POST':
        name = request.form['name']
        code = request.form['code']
        new_customer = Customer(name=name, code=code)
        db.session.add(new_customer)
        db.session.commit()
        return redirect(url_for('manage_customers'))
    
    customers = Customer.query.all()
    return render_template('customers.html', customers=customers)

@app.route('/orders', methods=['GET', 'POST'])
def manage_orders():
    if request.method == 'POST':
        item = request.form['item']
        amount = request.form['amount']
        time = request.form['time']
        customer_id = request.form['customer_id']
        new_order = Order(item=item, amount=amount, time=time, customer_id=customer_id)
        db.session.add(new_order)
        db.session.commit()
        
        customer = Customer.query.get(customer_id)
        sms.send(f'New order added: {item}, Amount: {amount}', [customer.code])
        
        return redirect(url_for('manage_orders'))
    
    orders = Order.query.all()
    customers = Customer.query.all()
    return render_template('orders.html', orders=orders, customers=customers)

if __name__ == '__main__':
    app.run(debug=True)
