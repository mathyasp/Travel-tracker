from sqlalchemy import PrimaryKeyConstraint
from sqlalchemy_utils import URLType
from flask_login import UserMixin
from travel_app.extensions import db
from travel_app.utils import FormEnum

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

class Trip(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    trip_type = db.Column(db.Enum(TripType), nullable=False)
    past_or_future = db.Column(db.Enum(PastOrFuture), nullable=False)
    country = db.relationship("Country", back_populates="trips")
    year = db.Column(db.Integer, nullable=False)
    trip_length = db.Column(db.Integer, nullable=False)
    highlight = db.Column(db.String(200), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    users = db.relationship("User", secondary="user_trips_table", back_populates="trips_taken")

    def __str__(self):
        return f"<TripType: {self.name}"
    
    def __repr__(self):
        return f"<TripType: {self.name}>"
class Country(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    climate = db.Column(db.Enum(ClimateType), nullable=False)
    language = db.Column(db.String(50), nullable=False)
    img_url = db.Column(URLType)
    trip_id = db.Column(db.Integer, db.ForeignKey("trip.id"), nullable=False)
    trips = db.relationship("Trip", back_populates="country")

    def __str__(self):
        return f"<Country: {self.name}"
    
    def __repr__(self):
        return f"<Country: {self.name}>"

class User(UserMixin, db.Model):
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(80), nullable=False, unique=True)
  password = db.Column(db.String(200), nullable=False)
  name = db.Column(db.String(80), nullable=False)
  profile_pic_url = db.Column(URLType)
  trips_taken = db.relationship("Trip", secondary="user_trips_table", back_populates="users")

  def __str__(self):
    return f"<User: {self.username}>"

  def __repr__(self):
    return f"<User: {self.username}>"

user_trips_table = db.Table("user_trips",
    db.Column("user_id", db.Integer, db.ForeignKey("user.id")),
    db.Column("trip_id", db.Integer, db.ForeignKey("trip.id")),
    PrimaryKeyConstraint("user_id", "trip_id")
)