from operator import not_
from flask import redirect, render_template, request, url_for, session, abort
from flask.helpers import flash
from app.models.puntos_encuentro import PuntosDeEncuentro
from app.models.user import User
from app.helpers.permission import check as check_permission
from app.helpers.email import check as check_email
from app.helpers.auth import authenticated
from app.db import db


# Protected resources
def index():
    user_email = authenticated(session)
    id = User.get_id_from_email(user_email)
    if not user_email:
        abort(401)
    if not check_permission(id, "punto_encuentro_index"):
        abort(401)
    puntos_encuentro = PuntosDeEncuentro.query.all()
    return render_template("puntos_encuentro/index.html", puntos_encuentro=puntos_encuentro)


def new():
    user_email = authenticated(session)
    id = User.get_id_from_email(user_email)
    if not user_email:
        abort(401)
    if not check_permission(id, "punto_encuentro_new"):
        abort(401)
    return render_template("puntos_encuentro/new.html", puntos_encuentro=None)


def create():
    if not authenticated(session):
        abort(401)
    if not check_email(request.form["email"]):
        flash("Ingrese un email valido")
        return render_template("puntos_encuentro/new.html", puntos_encuentro=request.form)
    if PuntosDeEncuentro.unique_fields(request.form):
        flash("Uno o mas campos ya se encuentra cargado en el sistema")
        return render_template("puntos_encuentro/new.html", puntos_encuentro=request.form)
    new_punto = PuntosDeEncuentro(**request.form)
    db.session.add(new_punto)
    db.session.commit()
    return redirect(url_for("puntos_encuentro_index"))

def search():
    user_email = authenticated(session)
    id = User.get_id_from_email(user_email)
    if not user_email:
        abort(401)
    if not check_permission(id, "punto_encuentro_index"):
        abort(401)
    puntos_encuentro = PuntosDeEncuentro.query.filter(PuntosDeEncuentro.name.like('%'+request.args["name"]+'%'))
    if request.args.getlist("active"):
        puntos_encuentro = puntos_encuentro.filter(PuntosDeEncuentro.state==False)
    if request.args.getlist("inactive"):
        puntos_encuentro = puntos_encuentro.filter(PuntosDeEncuentro.state==True)
    return render_template("puntos_encuentro/index.html", puntos_encuentro=puntos_encuentro)

    