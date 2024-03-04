import os
import unittest
from unittest import TestCase
import app
from datetime import date
from travel_app.extensions import app, db, bcrypt
from travel_app.models import Country, Trip, User, ClimateType, TripType, PastOrFuture

def create_user():
    password_hash = bcrypt.generate_password_hash('password').decode('utf-8')
    user = User(
      username='user_test', 
      password=password_hash, 
      name='Test User', 
      profile_pic_url='https://www.google.com/images/branding/googlelogo/1x/googlelogo_color_272x92dp.png'
    )
    db.session.add(user)
    db.session.commit()

class AuthTests(TestCase):
    """Tests for authentication (login & signup)."""
 
    def setUp(self):
        """Executed prior to each test."""
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app = app.test_client()
        db.drop_all()
        db.create_all()

    def test_signup(self):
        post_data = {
            'username': 'test_user',
            'password': 'test_password',
            'name': 'Test User',
            'profile_pic_url': 'https://www.google.com/images/branding/googlelogo/1x/googlelogo_color_272x92dp.png'
        }
        self.app.post('/signup', data=post_data)

        user = User.query.filter_by(username='test_user').one()
        self.assertIsNotNone(user)

    def test_signup_existing_user(self):
        create_user()

        post_data = {
            'username': 'user_test',
            'password': 'test_password',
            'name': 'Test User',
            'profile_pic_url': 'https://www.google.com/images/branding/googlelogo/1x/googlelogo_color_272x92dp.png'
        }
        response = self.app.post('/signup', data=post_data)

        self.assertIn(b'That username is taken. Please choose a different one.', response.data)

    def test_login_correct_password(self):
        create_user()

        post_data = {
            'username': 'user_test',
            'password': 'password'
        }
        response = self.app.post('/login', data=post_data) 
        self.assertNotIn(b'login', response.data)

    def test_login_nonexistent_user(self):
        post_data = {
            'username': 'user_test',
            'password': 'password'
        }
        response = self.app.post('/login', data=post_data)
        self.assertIn(b'No user with that username. Please try again.', response.data)

    def test_login_incorrect_password(self):
        create_user()

        post_data = {
            'username': 'user_test',
            'password': 'test_password'
        }
        response = self.app.post('/login', data=post_data)
        self.assertIn(b'Password doesn&#39;t match. Please try again.', response.data)

    def test_logout(self):
        create_user()

        post_data = {
            'username': 'user_test',
            'password': 'test_password'
        }
        self.app.post('/login', data=post_data)

        response = self.app.get('/logout')
        self.assertIn(b'login', response.data)
