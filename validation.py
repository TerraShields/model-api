from wtforms import Form, StringField, validators
from wtforms.validators import InputRequired


class PredictValidation(Form):
    latitude = StringField('latitude', validators=[InputRequired()])
    longitude = StringField('longitude', validators=[InputRequired()])
    sign = StringField('sign', validators=[InputRequired()])


class WithoutImage(Form):
    latitude = StringField('latitude', validators=[InputRequired()])
    longitude = StringField('longitude', validators=[InputRequired()])
    sign = StringField('sign', validators=[InputRequired()])
    caption = StringField('sign', validators=[InputRequired()])
