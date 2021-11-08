from flask import redirect, render_template, request, url_for, session, abort, flash
from sqlalchemy.exc import OperationalError
from app.forms.recorridos_evacuacion import CreateRecorrido, EditRecorrido
from app.models.recorridos_evacuacion import Recorridos
from app.helpers.auth import authenticated
from app.helpers.permission import has_permission as check_permission
from app.helpers.configuration import get_configuration

# Protected resources
def index(page):
    """
    Renderizado del listado de recorridos de evacuacion de forma paginada

    Args:
        page(int): número de pagina
    """
    user_email = authenticated(session)
    if not user_email:
        abort(401)

    if not check_permission("recorridos_index", session):
        abort(401)

    # mostramos listado paginado:
    # row con config actual
    config = get_configuration(session) 
    try:
        recorridos = Recorridos.get_index_recorridos(page, config)
    except OperationalError:
        flash("No hay recorridos aún.")
        recorridos = None
    return render_template("recorridos_evacuacion/index.html", recorridos=recorridos)

def new():
    """
    Renderizado de la página de creación de un recorrido
    """
    user_email = authenticated(session)
    if not user_email:
        abort(401)
    if not check_permission("recorridos_new", session):
        abort(401)
    form = CreateRecorrido()
    return render_template("recorridos_evacuacion/new.html", form=form)


def create():
    """
    Lógica a realizar al momento de confirmar
    la creación de un recorrido 
    """
    user_email = authenticated(session)
    if not user_email:
        abort(401)
    form = CreateRecorrido(request.form)
    if form.validate():
        recorrido = Recorridos.unique_field(form.name)
        if recorrido:
            flash("Ya existe un recorrido con ese nombre. Ingrese uno nuevo.")
            return render_template("recorridos_evacuacion/new.html", form=form)
        else:
            new_recorrido = Recorridos(name=form.name.data, description=form.description.data, coords=form.coordinates)
            Recorridos.add_recorrido(new_recorrido)
            Recorridos.update()
            flash("El recorrido ha sido creado correctamente.")
            return render_template("recorridos_evacuacion/new.html", form=form)
    return render_template("recorridos_evacuacion/new.html", form=form)


def edit():
    """
    Renderizado de la página de edición de un recorrido
    """
    user_email = authenticated(session)
    if not user_email:
        abort(401)
    if not check_permission("recorridos_edit", session):
        abort(401)
    recorrido = Recorridos.get_recorrido_by_id(request.form['id'])
    form = EditRecorrido(id=recorrido.id)
    return render_template("recorridos_evacuacion/edit.html", form=form)


def update():
    """
    Lógica a realizar al momento de confirmar
    la edición de un recorrido 
    """
    user_email = authenticated(session)
    if not user_email:
        abort(401)
    if not check_permission("recorridos_update", session):
        abort(401)
    form = EditRecorrido(request.form)
    if form.validate():
        recorrido = Recorridos.get_recorrido_by_id(form.id.data)
        query = Recorridos.get_recorrido_by_name(form.name.data)
        if query and query.id!=recorrido.id:
            flash("Ya existe un recorrido con ese nombre")
            return render_template("recorridos_evacuacion/edit.html", form=form)
        recorrido.edit(name=form.name.data, description=form.description.data, lat=form.lat.data, long=form.long.data)
        recorrido.update()
        return redirect(url_for("recorridos_index"))
    return render_template("recorridos_evacuacion/edit.html", form=form)


def delete():
    """
    Lógica a realizar al momento de eliminar
    de manera fisica a un recorrido

    Args:
        id(int): id del recorrido a eliminar
    """
    user_email = authenticated(session)
    if not user_email:
        abort(401)
    if not check_permission('recorridos_destroy', session):
        abort(401)
    recorrido = Recorridos.get_recorrido_by_id(request.form["id"])
    recorrido.delete()
    recorrido.update()
    flash("Recorrido eliminado correctamente.")
    return redirect(url_for("recorridos_index"))

def change_state(id):
    """
    Lógica a realizar al momento de modificar el
    estado de un recorrido.

    Args:
        id(int): id del usuario 
    """
    user_email = authenticated(session)
    if not user_email:
        abort(401)
    if not check_permission('recorridos_publicate', session):
        abort(401)
    recorrido = Recorridos.get_recorrido_by_id(id)
    recorrido.change_state()
    state = "publicado" if recorrido.state else "despublicado"
    recorrido.update()
    flash("El recorrido ha sido {} correctamente".format(state))
    return redirect(url_for("recorridos_index"))

def search(page):
    """
    Lógica a realizar al momento de renderizar
    un listado de búsqueda de recorridos paginado.

    Args:
        page(int): número de página
    """
    user_email = authenticated(session)
    if not user_email:
        abort(401)
    if not check_permission("recorridos_index",session):
        abort(401)
    config = get_configuration(session) 
    recorridos = Recorridos.search_by_name(name=request.args["name"])
    parameters = {
        "name": request.args["name"],
        "state": "",
    }
    if "state" in request.args.keys():
        parameters["state"] == request.args["state"]
        if request.args["state"]=="publicado":
            recorridos = Recorridos.get_with_state(recorridos, True)
        else:
            recorridos = Recorridos.get_with_state(recorridos, False)
    recorridos =  Recorridos.search_paginate(recorridos, page=page, config=config)
    return render_template("recorridos_evacuacion/index.html", recorridos=recorridos, filter=1, parameters=parameters)

def show(name):
    """
    Renderiza el detalle con los datos de un dado recorrido

    Args:
        name(string): nombre del recorrido a detallar
    """
    user_email = authenticated(session)
    if not user_email:
        abort(401)
    if not check_permission("recorridos_show", session):
        abort(401)
    
    recorrido = Recorridos.get_recorrido_by_name(name=name)
    return render_template("recorridos_evacuacion/show.html", recorrido=recorrido)
