from flask_wtf import FlaskForm
from wtforms import StringField, DateField, FloatField, SelectField, SubmitField, ValidationError
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired, Length, NumberRange
from travel_app.models import Country, Trip, User, TripType, PastOrFuture, ClimateType

class CountryForm(FlaskForm):
    name = StringField("Country Name", 
      validators=[
        DataRequired(), 
        Length(min=2, max=50)
      ])
    climate = StringField("Climate", 
      validators=[
        DataRequired(), 
        Length(min=2, max=50)
      ])
    language = StringField("Language", 
      validators=[
        DataRequired(), 
        Length(min=2, max=50)
      ])
    img_url = StringField("Image URL", 
      validators=[
        DataRequired()
      ])
    submit = SubmitField("Submit")

class TripForm(FlaskForm):
    trip_type = SelectField("Trip Type", 
      choices=TripType.choices(), 
      validators=[
        DataRequired()
      ])
    past_or_future = SelectField("Past or Future", 
      choices=PastOrFuture.choices(), 
      validators=[
        DataRequired()
      ])
    country = QuerySelectField("Country", 
      query_factory=lambda: Country.query, 
      allow_blank=False, 
      get_label="name")
    year = DateField("Year", 
      validators=[
        DataRequired()
      ])
    trip_length = FloatField("Trip Length", 
      validators=[
        DataRequired(), 
        NumberRange(min=1, max=365)
      ])
    highlight = StringField("Highlight", 
      validators=[
        DataRequired(), 
      ])
    submit = SubmitField("Submit")

    def validate_highlight(form, field):
      """Validate time format in the form 'Xd, Xw, Xm' (X days, X weeks, X months)"""
      time_units = field.data.split(',')
      for unit in time_units:
        unit = unit.strip()
        if not (unit.endswith('d') or unit.endswith('w') or unit.endswith('m')):
          raise ValidationError('Time must be in the format "Xd, Xw, Xm"')
        try:
          int(unit[:-1])
        except ValueError:
          raise ValidationError('Time must be in the format "Xd, Xw, Xm"')