from wtforms import Form, StringField, SubmitField
from wtforms.validators import Required

class SearchForm(Form):
    key_word = StringField('Key-word search term') #, validators=[Required()]
    submit = SubmitField('Submit')