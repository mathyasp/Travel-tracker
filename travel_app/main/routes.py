from flask import Blueprint, request, render_template, redirect, url_for, flash
from datetime import date, datetime
from flask_login import login_required, current_user
from travel_app.models import Country, Trip, User
from travel_app.main.forms import CountryForm, TripForm

from travel_app.extensions import app, db

main = Blueprint("main", __name__)

@main.route("/")
def index():
    all_trips = Trip.query.all()
    print(current_user)
    return render_template("index.html", all_trips=all_trips)

@main.route("/add_trip", methods=["GET", "POST"])
@login_required
def add_trip():
    form = TripForm()
    if form.validate_on_submit():
        new_trip = Trip(
            trip_type=form.trip_type.data,
            past_or_future=form.past_or_future.data,
            country=form.country.data,
            year=form.year.data,
            trip_length=form.trip_length.data,
            highlight=form.highlight.data,
        )
        db.session.add(new_trip)
        db.session.commit()

        flash("Your trip has been added!")
        return redirect(url_for("main.trip_detail", trip_id=new_trip.id))
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