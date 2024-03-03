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
    climate = SelectField("Climate Type", 
      choices=ClimateType.choices(), 
      validators=[
        DataRequired()
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
    date_arrived = DateField("Date Arrived", 
      validators=[
        DataRequired()
      ])
    trip_length = StringField("Trip Length", 
      validators=[
        DataRequired(),
      ])
    highlight = StringField("Highlight", 
      validators=[
        DataRequired(),
        Length(min=2, max=200)
      ])
    submit = SubmitField("Submit")

    def validate_trip_length(form, field):
      """Validate time format in the form '7 days', '2 weeks', '1 month and 5 days'"""
      time_units = field.data.split('and')
      for unit in time_units:
        unit = unit.strip()
        number, time_unit = unit.split(' ')
        if not (time_unit in ['day', 'days', 'week', 'weeks', 'month', 'months']):
          raise ValidationError('Time must be in the format "7 days", "2 weeks", "1 month and 5 days"')
        try:
          int(number)
        except ValueError:
          raise ValidationError('Time must be in the format "7 days", "2 weeks", "1 month and 5 days"')