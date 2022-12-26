from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField

def FormCompetitionsSearch(levels, cities):
    class _FormCompetitionsSearch(FlaskForm):
        level_choices = [("-1", "")] + \
            [(level.id, level.description) for level in levels]
        level = SelectField("Уровень", choices=level_choices)
        city_choices = [("-1", "")] + \
            [(city.city, city.city) for city in cities]
        city = SelectField("Город", choices=city_choices)
        submit = SubmitField("Поиск")
    return _FormCompetitionsSearch()