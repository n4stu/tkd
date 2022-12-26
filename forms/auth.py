from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import Email, Length

class FormUserAuth(FlaskForm):
    login = StringField("Логин:", validators=[Length(2, -1, "Логин не может быть короче 2 символов")])
    pswd = PasswordField("Пароль:", validators=[Length(4, -1, "Пароль не может быть короче 4 символов")])
    submit = SubmitField("Войти")