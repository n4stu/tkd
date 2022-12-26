from flask import Flask, render_template, request, redirect, g, flash, url_for
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_menu import Menu, register_menu

from forms.auth import *
from forms.sportsman_weight import *
from forms.competitions_search import *
from forms.clubs_search import *
from forms.competiotion_sportsmans import *

from user_login import *
from dotmap import DotMap
from db import *
import psycopg2

table = "sportsman"
app = Flask(__name__)
app.config["SECRET_KEY"] = "dgfoifs3824234jdgflk3428"
app.jinja_env.trim_blocks = True
Menu(app=app)
login_manager = LoginManager(app=app)
login_manager.login_view = "auth"
login_manager.login_message = "Для доступа требуется авторизация"
login_manager.login_message_category = "danger"

#print("ХЕШ", generate_password_hash("pencil_23"))

@app.route("/", methods=["POST", "GET"])
@register_menu(app, ".index", "Инфо", order=0)
@login_required
def index():
    form = FormSportsmanEdit()
    if table == "sportsman":
        weight = current_user.user.weight
        form = FormSportsmanEdit(weight)    
    if form.validate_on_submit():
        sportsman_id = current_user.user.id
        db.sportsman_update_weight(sportsman_id, form.weight.data)
        flash("Вес обновлен", "success")
    return render_template("show_profile.htm", form=form)

@app.route("/competitions", methods=["POST", "GET"])
@register_menu(app, ".competitions", "Соревнования", order=1)
@login_required
def competitions():
    levels = db.get_competitions_levels()
    cities = db.get_competitions_cities()
    form = FormCompetitionsSearch(levels, cities)
    filters = DotMap({
        "level": form.level.data if form.level.data != "-1" else None,
        "city": form.city.data if form.city.data != "-1" else None
    })
    competitions = db.get_filtered_competitions(filters)
    return render_template("show_competitions.htm",
        table=table,
        form=form,
        competitions=competitions
    )

@app.route("/competitions/<int:competition_id>", methods=["POST", "GET"])
@login_required
def competitions_show(competition_id):
    if table != "coach":
        return redirect(url_for("competitions"))
    if request.args.get("add"):
        sportsman_id = request.args.get("add")
        db.update_request(competition_id, current_user.user.id, sportsman_id, True)
    if request.args.get("delete"):
        sportsman_id = request.args.get("delete")
        db.update_request(competition_id, current_user.user.id, sportsman_id, False)
    competition = db.get_competition_by_id(competition_id)
    c_sportsmans = db.get_coach_sportsmans(current_user.user.id)
    r_sportsmans = db.get_request_sportsmans(competition_id)
    s_ids = []
    if r_sportsmans:
        s_ids = [sportsman.sportsman_id for sportsman in r_sportsmans]
    return render_template("show_competition.htm",
        competition=competition,
        c_sportsmans=c_sportsmans,
        r_sportsmans=r_sportsmans,
        s_ids=s_ids
    )

@app.route("/clubs", methods=["POST", "GET"])
@register_menu(app, ".clubs", "Клубы", order=2)
@login_required
def clubs():
    cities = db.get_clubs_cities()
    form = FormClubsSearch(cities)
    clubs = db.get_filtered_clubs(DotMap({
        "city": form.city.data if form.city.data != "-1" else None
    }))
    return render_template("show_clubs.htm", form=form, clubs=clubs)

@app.route("/sportsmans", methods=["POST", "GET"])
@register_menu(app, ".sportsmans", "Спортсмены", order=3)
@login_required
def sportsmans():
    if table != "coach":
        return redirect(url_for("index"))
    
    sportsmans = db.get_coach_sportsmans(current_user.user.id)
    return render_template("show_sportsmans.htm", sportsmans=sportsmans)

@app.route("/auth", methods=["POST", "GET"])
def auth():
    global table
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = FormUserAuth()
    if form.validate_on_submit():
        data = DotMap({ "login": form.login.data })
        sportsman = db.get_sportsman_by_login(data)
        if sportsman and check_password_hash(sportsman.password, form.pswd.data):
            table = "sportsman"
            user_login = UserLogin().create(sportsman)
            login_user(user_login)
            return redirect(url_for("index"))
        coach = db.get_coach_by_login(data)
        if coach and check_password_hash(coach.password, form.pswd.data):
            table = "coach"
            user_login = UserLogin().create(coach)
            login_user(user_login)
            return redirect(url_for("index"))
        form.login.errors.append("Логин или пароль введен неверно")
    return render_template("auth.htm", form=form)
    
@app.route("/logout")
@login_required
def logout():
    if current_user.is_authenticated:
        global table
        logout_user()
        table = "sportsman"
        flash("Вы вышли из учетной записи", "success")
    return redirect(url_for("auth"))

@app.context_processor
def context_processor():
    global table
    if current_user.is_authenticated:
        return dict(user=current_user.user, table=table)
    return dict(table=table)

db = None
@app.before_request
def before_request():
    global db
    db = DB(get_db())
    

@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'link_db'):
        g.link_db.close()

def connect_db():
    return psycopg2.connect("dbname=tkd_system user=postgres password=1234 host=localhost")

def get_db():
    if not hasattr(g, "link_db"):
        g.link_db = connect_db()
    return g.link_db

@login_manager.user_loader
def load_user(user_id):
    global table
    if current_user and not hasattr(current_user.user, "passport_no"):
        table = "coach"
    return UserLogin().fromDB(user_id, db, table)

if __name__ == "__main__":
    app.run(debug=True)
    