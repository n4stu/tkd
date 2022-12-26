from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField

def FormClubsSearch(cities):
    class _FormClubsSearch(FlaskForm):
        city_choices = [("-1", "")] + \
            [(city.city, city.city) for city in cities]
        city = SelectField("Город", choices=city_choices)
        submit = SubmitField("Поиск")
    return _FormClubsSearch()