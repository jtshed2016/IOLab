from app import db

#helper table (associative entity?) for many-to-many relationship b/t custs and orders
#not sure if this is correct...have not been able to successfully implement
order_relationship = db.Table('order_relationship',
    db.Column('cust_id', db.Integer, db.ForeignKey('customer.id')),
    db.Column('order_id', db.Integer, db.ForeignKey('order.id'))
)


class Customer(db.Model):
    #__tablename__ = 'Customer'
    id = db.Column(db.Integer, primary_key=True)
    company = db.Column(db.String(120), unique=False)
    email = db.Column(db.String(120))
    phone = db.Column(db.String(12))
    addresses = db.relationship('Address', backref='customer', lazy='select')
    orders = db.relationship('Order', secondary=order_relationship, 
        backref=db.backref('customers', lazy='dynamic'))
    # see http://flask-sqlalchemy.pocoo.org/2.1/models/#one-to-many-relationships

    def __repr__(self):
        return '<Customer %r>' % self.email

# Your Address code should go here
class Address(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    streetno = db.Column(db.Integer)
    streetname = db.Column(db.String(40))
    city = db.Column(db.String(50))
    state = db.Column(db.String(2))
    zipcode = db.Column(db.Integer)
    current = db.Column(db.Boolean)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'))
    def __repr__(self):
        return '<Address %i %r' % (self.streetno, self.streetname)

class Order(db.Model):
    #__tablename__ ='Order'
    id = db.Column(db.Integer, primary_key=True)
    total_spent = db.Column(db.Float(scale=2))
    num_parts_ordered = db.Column(db.Integer)


    def __repr__(self):
        return '<Order %r>' %self.id


