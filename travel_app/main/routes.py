from flask import Blueprint, request, render_template, redirect, url_for, flash
from datetime import date, datetime
from flask_login import login_required, current_user
from travel_app.models import Country, Trip, User
from travel_app.main.forms import CountryForm, TripForm

from travel_app.extensions import app, db

main = Blueprint("main", __name__)

@main.route("/")
def index():
    all_countries = Country.query.all()
    return render_template("index.html", all_countries=all_countries)

@main.route("/add_trip", methods=["GET", "POST"])
@login_required
def add_trip():
    form = TripForm()
    if form.validate_on_submit():
        add_trip = Trip(
            trip_name=form.trip_name.data,
            trip_type=form.trip_type.data,
            past_or_future=form.past_or_future.data,
            country=form.country.data,
            date_arrived=form.date_arrived.data,
            trip_length=form.trip_length.data,
            highlight=form.highlight.data,
            user_id=current_user.id,
        )
        current_user.trips_taken.append(add_trip)
        db.session.add(add_trip)
        db.session.commit()

        flash("Your trip has been added!")
        return redirect(url_for("main.trip_page", trip_id=add_trip.id))
    return render_template("add_trip.html", form=form)

@main.route("/add_country", methods=["GET", "POST"])
@login_required
def add_country():
    form = CountryForm()
    if form.validate_on_submit():
        new_country = Country(
            name=form.name.data,
            climate=form.climate.data,
            language=form.language.data,
            img_url=form.img_url.data,
        )
        db.session.add(new_country)
        db.session.commit()
        return redirect(url_for("main.index"))
    return render_template("add_country.html", form=form)

@main.route("/trip/<trip_id>", methods=['GET', 'POST'])
def trip_page(trip_id):
    trip = Trip.query.get(trip_id)
    form = TripForm(obj=trip)

    if form.validate_on_submit():
        trip.trip_name = form.trip_name.data
        trip.trip_type = form.trip_type.data
        trip.past_or_future = form.past_or_future.data
        trip.country = form.country.data
        trip.date_arrived = form.date_arrived.data
        trip.trip_length = form.trip_length.data
        trip.highlight = form.highlight.data
        trip.users = form.users.data

        db.session.commit()

        flash("Your trip has been updated!")
        return redirect(url_for("main.trip_page", trip_id=trip_id))
        
    return render_template("trip_page.html", trip=trip, form=form)

@main.route("/country/<country_id>", methods=['GET', 'POST'])
def country_page(country_id):
    country = Country.query.get(country_id)
    form = CountryForm(obj=country)

    if form.validate_on_submit():
        country.name = form.name.data
        country.climate = form.climate.data
        country.language = form.language.data
        country.img_url = form.img_url.data
        db.session.commit()
        flash("Your country has been updated!")
        return redirect(url_for("main.country_page", country_id=country.id))
    return render_template("country_page.html", country=country, form=form)

@main.route('/user_page/<username>')
@login_required
def user_page(username):
    user = User.query.filter_by(username=username).one()
    return render_template('user_page.html', user=user)
