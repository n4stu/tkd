from flask_wtf import FlaskForm
from wtforms import SubmitField, Form, FieldList, FormField, SelectField, BooleanField

def FormCompetitionSportsmans(sportsmans, request_sportsmans):

    class SportsmanField(Form):
        sportsman = BooleanField("111", default=False)

    class _FormCompetitionSportsmans(FlaskForm):
        # sportsmansFields = []
        # for sportsman in sportsmans:
        #     label = sportsman.name + " (Вес: " + str(sportsman.weight) + " кг)"
        #     sportsmansFields.append(BooleanField(label, default=False))

        sportsmans = FieldList(FormField(SportsmanField) , min_entries=5)

        # BooleanField("Задолженность", default=False)

        submit = SubmitField("Поиск")
    return _FormCompetitionSportsmans()