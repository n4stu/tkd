from flask_wtf import FlaskForm
from wtforms import SubmitField, IntegerField
from wtforms.validators import NumberRange

def FormSportsmanEdit(w = 0):
    class _FormSportsmanEdit(FlaskForm):
        weight = IntegerField("Вес (кг): ", default=w, validators=[NumberRange(30, 130, "Вес не может быть меньше 30 и более 130 килограмм")])
        submit = SubmitField("Сохранить")
    return _FormSportsmanEdit()