from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField, StringField, FloatField, SelectField
from wtforms.validators import DataRequired


class TextForm(FlaskForm):
    money = FloatField('Money', validators=[DataRequired()])
    currencies = SelectField('Currencies', choices=[('840', 'USD'), ('978', 'EUR')])
    description = TextAreaField('Description', validators=[DataRequired()])
    buy = SubmitField('Buy')