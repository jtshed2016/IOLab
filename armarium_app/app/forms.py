from flask.ext.wtf import Form
from wtforms import StringField, IntegerField, SelectField, FloatField
from flask_wtf.html5 import EmailField
from wtforms.validators import DataRequired, InputRequired

class MsForm(Form):
	shelfmark = StringField('shelfmark', validators=[DataRequired()])
	mstitle = StringField('mstitle', validators=[DataRequired()])
	mstitle_var = StringField('mstitle')