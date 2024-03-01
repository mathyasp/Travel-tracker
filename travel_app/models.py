from sqlalchemy import PrimaryKeyConstraint
from sqlalchemy_utils import URLType
from flask_login import UserMixin
from grocery_app.extensions import db
from grocery_app.utils import FormEnum

class ClimateType(FormEnum):
  """Different climate types"""
  tropical = "Tropical"
  arid = "Arid"
  temperate = "Temperate"
  continental = "Continental"
  polar = "Polar"

class TripType(FormEnum):
  """Different trip types"""
  leisure = "Leisure"
  business = "Business"
  family = "Family"
  adventure = "Adventure"

class PastOrFuture(FormEnum):
  """Past or future trip"""
  past = "Past"
  future = "Future"

class Country(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    climate = db.Column(db.String(50), nullable=False)
    language = db.Column(db.String(50), nullable=False)
    img_url = db.Column(URLType)

    def __str__(self):
        return f"<Country: {self.name}"
    
    def __repr__(self):
        return f"<Country: {self.name}>"

class Trip(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    trip_type = db.Column(db.String(50), nullable=False)
    past_or_future = db.Column(db.String(50), nullable=False)
    country = db.relationship("Country", back_populates="country")
    year = db.Column(db.Integer, nullable=False)
    trip_length = db.Column(db.Integer, nullable=False)
    highlight = db.Column(db.String(200), nullable=False)

    def __str__(self):
        return f"<TripType: {self.name}"
    
    def __repr__(self):
        return f"<TripType: {self.name}>"

class User(UserMixin, db.Model):
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(80), nullable=False, unique=True)
  password = db.Column(db.String(200), nullable=False)
  name = db.Column(db.String(80), nullable=False)
  profile_pic_url = db.Column(URLType)
  trips = db.relationship("Trip", secondary=user_trips_table, back_populates="trips")

  def __str__(self):
    return f"<User: {self.username}>"

  def __repr__(self):
    return f"<User: {self.username}>"

user_trips_table = db.Table("user_trips",
    db.Column("user_id", db.Integer, db.ForeignKey("user.id")),
    db.Column("trip_id", db.Integer, db.ForeignKey("trip.id")),
    PrimaryKeyConstraint("user_id", "trip_id")
)