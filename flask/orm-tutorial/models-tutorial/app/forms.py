from flask.ext.wtf import Form
from wtforms import StringField, IntegerField, SelectField, FloatField
from flask_wtf.html5 import EmailField
from wtforms.validators import DataRequired

class CustomerForm(Form):
    company = StringField('company', validators=[DataRequired()])
    email = EmailField('email', validators=[DataRequired()])
    phone = StringField('phone', validators=[DataRequired()])
    streetno = IntegerField('streetno', validators=[DataRequired()])
    streetname = StringField('streetname', validators=[DataRequired()])
    city = StringField('city', validators=[DataRequired()])
    state = StringField('state', validators=[DataRequired()])
    zipcode = IntegerField('zipcode', validators=[DataRequired()])
   
class AddressForm(Form):
    company_name = SelectField('company_name', coerce=int, validators=[DataRequired()])
    #this is a misnomer...should be "company_id" but whatevs
    streetno = IntegerField('streetno', validators=[DataRequired()])
    streetname = StringField('streetname', validators=[DataRequired()])
    city = StringField('city', validators=[DataRequired()])
    state = StringField('state', validators=[DataRequired()])
    zipcode = IntegerField('zipcode', validators=[DataRequired()])

class OrderForm(Form):
    company_name = SelectField('company_name', coerce=int, validators=[DataRequired()])
    #this is a misnomer...should be "company_id" but whatevs
    total_spent = FloatField('total_spent', validators = [DataRequired()])
    num_parts_ordered = IntegerField('num_parts_ordered', validators = [DataRequired()])