import os
import unittest
import app
from datetime import date
from travel_app.extensions import app, db, bcrypt
from travel_app.models import Country, Trip, User, ClimateType, TripType, PastOrFuture

def login(client, username, password):
    return client.post('/login', data={
        'username': username, 
        'password': password
    }, follow_redirects=True)

def logout(client):
    return client.get('/logout', follow_redirects=True)

def add_trip():
    country = Country(
      name='Test Country', 
      climate=ClimateType.temperate, 
      language='English',
      img_url='https://www.google.com/images/branding/googlelogo/1x/googlelogo_color_272x92dp.png'
    )
    trip = Trip(
      trip_name='Test Trip',
      trip_type=TripType.leisure,
      past_or_future=PastOrFuture.future,
      country=country,
      date_arrived=date(2021, 1, 1),
      trip_length='7 days',
      highlight='Test Highlight'
    )
    db.session.add(trip)
    db.session.commit()


def add_user():
    password_hash = bcrypt.generate_password_hash('password').decode('utf-8')
    user = User(
      username='user_test', 
      password=password_hash, 
      name='Test User', 
      profile_pic_url='https://www.google.com/images/branding/googlelogo/1x/googlelogo_color_272x92dp.png'
    )
    db.session.add(user)
    db.session.commit()


class MainTests(unittest.TestCase):

    def setUp(self):
        """Executed prior to each test."""
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app = app.test_client()
        db.drop_all()
        db.create_all()

    def test_index_logged_out(self):
        """Test that the trip shows up on the homepage."""

        add_trip()
        add_user()

        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        response_test = response.get_data(as_text=True)
        self.assertIn('Test Trip', response_test)
        self.assertIn('Test Country', response_test)
        self.assertIn('Future', response_test)
        self.assertIn('Test Highlight', response_test)
        self.assertIn('https://www.google.com/images/branding/googlelogo/1x/googlelogo_color_272x92dp.png', response_test)
        self.assertIn('Log In', response_test)
        self.assertIn('Sign Up', response_test)

        self.assertNotIn('New Trip', response_test)
        self.assertNotIn('New Country', response_test)

    def test_index_logged_in(self):
        """Test that the trip shows up on the homepage."""

        add_trip()
        add_user()

        login(self.app, 'user_test', 'password')

        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        response_test = response.get_data(as_text=True)
        self.assertIn('Test Trip', response_test)
        self.assertIn('Test Country', response_test)
        self.assertIn('Future', response_test)
        self.assertIn('Test Highlight', response_test)
        self.assertIn('https://www.google.com/images/branding/googlelogo/1x/googlelogo_color_272x92dp.png', response_test)
        self.assertIn('Log Out', response_test)

        self.assertNotIn('Log In', response_test)
        self.assertNotIn('Sign Up', response_test)

    def test_trip_page_logged_out(self):
        """Test that the trip page shows up correctly."""

        add_trip()
        add_user()
        logout(self.app)

        response = self.app.get('/trip/1', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        response_test = response.get_data(as_text=True)
        self.assertIn('Test Country', response_test)
        self.assertIn('Test Country', response_test)
        self.assertIn('Future', response_test)
        self.assertIn('Test Highlight', response_test)
        self.assertIn('https://www.google.com/images/branding/googlelogo/1x/googlelogo_color_272x92dp.png', response_test)
        self.assertIn('Log In', response_test)
        self.assertIn('Sign Up', response_test)

        self.assertNotIn('Edit', response_test)

    def test_trip_page_logged_in(self):
        """Test that the trip page shows up correctly."""

        add_trip()
        add_user()

        login(self.app, 'user_test', 'password')

        response = self.app.get('/trip/1', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        response_test = response.get_data(as_text=True)
        self.assertIn('Test Country', response_test)
        self.assertIn('Test Country', response_test)
        self.assertIn('Future', response_test)
        self.assertIn('Test Highlight', response_test)
        self.assertIn('https://www.google.com/images/branding/googlelogo/1x/googlelogo_color_272x92dp.png', response_test)

        self.assertIn('Edit', response_test)

    def test_update_trip(self):
        """Test updating a trip."""

        add_trip()
        add_user()

        login(self.app, 'user_test', 'password')

        country = Country.query.get(1)
        post_data = {
            'trip_name': 'Test Trip',
            'trip_type': 'leisure',
            'past_or_future': 'future',
            'country': country.id,
            'date_arrived': '2021-01-01',
            'trip_length': '7 days',
            'highlight': 'Updated Highlight'
        }

        self.app.post('/trip/1', data=post_data)

        trip = Trip.query.get(1)
        
        self.assertEqual(trip.highlight, 'Updated Highlight')

    def test_add_trip(self):
        """Test creating a trip."""

        add_trip()
        add_user()

        login(self.app, 'user_test', 'password')

        country = Country(
            name='Another Test Country', 
            climate=ClimateType.tropical, 
            language='Spanish',
            img_url='https://www.example.com/images/branding/examplelogo/1x/examplelogo_color_272x92dp.png'
        )
        db.session.add(country)
        db.session.commit()

        post_data = {
                'trip_name': 'Another Test Trip',
                'trip_type': 'business',
                'past_or_future': 'past',
                'country': country.id,
                'date_arrived': '2022-01-01',
                'trip_length': '5 days',
                'highlight': 'Another Test Highlight'
        }

        self.app.post('/add_trip', data=post_data)

        trip = Trip.query.filter_by(trip_name='Another Test Trip').one()
        self.assertIsNotNone(trip)
        self.assertEqual(trip.country.name, 'Another Test Country')

    def test_add_trip_logged_out(self):
        """Test adding a trip while logged out."""

        add_trip()
        add_user()

        response = self.app.get('/add_trip')

        self.assertEqual(response.status_code, 302)
        self.assertIn('/login?next=%2Fadd_trip', response.location)

    

    def test_add_country(self):
        """Test adding a country."""

        add_trip()
        add_user()

        login(self.app, 'user_test', 'password')

        post_data = {
            'name': 'Another Test Country',
            'climate': 'tropical',
            'language': 'Spanish',
            'img_url': 'https://www.example.com/images/branding/examplelogo/1x/examplelogo_color_272x92dp.png'
        }

        self.app.post('/add_country', data=post_data)

        country = Country.query.filter_by(name='Another Test Country').one()
        self.assertIsNotNone(country)
        self.assertEqual(country.language, 'Spanish')

    def test_user_page(self):
        """Test that the user page shows up correctly."""

        add_trip()
        add_user()

        login(self.app, 'user_test', 'password')

        response = self.app.get('/user_page/user_test', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        response_test = response.get_data(as_text=True)
        self.assertIn('Test User', response_test)
        self.assertIn('https://www.google.com/images/branding/googlelogo/1x/googlelogo_color_272x92dp.png', response_test)
        self.assertIn('Log Out', response_test)

        self.assertNotIn('Log In', response_test)
        self.assertNotIn('Sign Up', response_test)