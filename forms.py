from flask_wtf import FlaskForm
from  wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, URL

choices = ['✅' '❌']

class Search(FlaskForm):
    location = StringField('Location', validators=[DataRequired()])
    submit = SubmitField('Search')

class Add(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    map_url = StringField('Map Link', validators=[DataRequired(), URL()])
    img_url = StringField("Image Link", validators=[DataRequired(), URL()])
    location = StringField('Location', validators=[DataRequired()])
    seats = StringField('Seats', validators=[DataRequired()])
    has_toilet = SelectField('Has Toilet', choices=choices, validators=[DataRequired()])
    has_sockets = SelectField('Has Sockets', choices=choices, validators=[DataRequired()])
    has_wifi = SelectField('Has wifi', choices=choices, validators=[DataRequired()])
    can_take_calls = SelectField('Can Take Calls', choices=choices, validators=[DataRequired()])
    coffee_price = StringField('Coffee Price', validators=[DataRequired()])
    submit = SubmitField('Add')

class Update(FlaskForm):
    seats = StringField('Seats', validators=[DataRequired()])
    has_toilet = SelectField('Has Toilet', choices=choices, validators=[DataRequired()])
    has_sockets = SelectField('Has Sockets', choices=choices, validators=[DataRequired()])
    has_wifi = SelectField('Has wifi', choices=choices, validators=[DataRequired()])
    can_take_calls = SelectField('Can Take Calls', choices=choices, validators=[DataRequired()])
    coffee_price = StringField('Coffee Price', validators=[DataRequired()])
    submit = SubmitField('Update')
    
