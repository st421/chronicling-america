from wtforms import Form, StringField, SelectField, SubmitField, validators
from wtforms.validators import DataRequired, Length

AVAILABLE_DIG_YEARS = range(1836,1924,4)
DIG_YEAR_CHOICES = [(i, i) for i in AVAILABLE_DIG_YEARS]
DIG_YEAR_CHOICES.insert(0, (0, ''))

class SearchForm(Form):
    year = SelectField('Election year', [DataRequired()], choices=DIG_YEAR_CHOICES, coerce=int, default=0)
    submit = SubmitField('Submit')