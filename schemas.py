from app import ma
from models import Customer, Order

class CustomerSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Customer

class OrderSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Order
