# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a sample controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
## - api is an example of Hypermedia API support and access control
#########################################################################

@auth.requires_login()
def index():
    if not session.s:
        redirect(URL('setsession'))
    else:
        redirect(URL('scan'))

def asigna_sesion(id):
    session.s=None
    session.s=db.sesion(id)
    if session.s:
        redirect(URL('scan'))
    else:
        redirect(URL('setsession'))
    return

@auth.requires(auth.has_membership(role='procesar'))
def descargar_sesion():
    if not request.args(0, cast=int):
        redirect(URL('setsession'))
    session.s=db.sesion(request.args(0,cast=int))
    if session.s:
        if session.s.estado != 'escaneando' :
            form= FORM.confirm('Descargar', {'Regresar':URL('setsession')})
            count = db(db.barcode.sesion==session.s.id).count()
            if form.accepted:
                session.s.update_record(estado='descargada')
                session.flash = 'Sesion ' + str( session.s.id) + ' descargada'
                filename = 'sesion_escaneo_%s.csv' % str(session.s.id)
                rows = db(db.barcode.sesion == session.s.id).select(db.barcode.sesion,db.barcode.codigo,db.barcode.modified_by,db.barcode.modified_on)
                response.view ='default/descargar_sesion.csv'
                return dict(rows=rows,filename=filename)
            return dict(row=session.s, form=form, count=count)
        else:
            session.flash='Antes de Descargar la sesion es necesario cerrarla (Terminarla)'
            redirect(URL('cerrar_sesion'))
    else:
        session.flash='Sesion invalida'
        redirect(URL('setsession'))

@auth.requires(auth.has_membership(role='capturar'))
def cerrar_sesion():
    if not session.s or session.s.estado != 'escaneando':
        redirect(URL('setsession'))
    else:
        form= FORM.confirm('Confirmar', {'Regresar':URL('setsession')})
        row=db.sesion(session.s.id)
        count = db(db.barcode.sesion == session.s.id).count()
        if form.accepted:
            row.update_record(estado='cerrada')
            session.flash = 'Sesion ' + str(session.s.id) + ' cerrada'
            redirect(URL('setsession'))
        return dict(row=row, form=form, count=count)


@auth.requires(auth.has_membership(role='procesar'))
def crear_tiposesion():
    grid=SQLFORM.grid(db.tiposesion)
    return locals()

@auth.requires(auth.has_membership(role='capturar') or auth.has_membership(role='procesar'))
def sesion():
    db.sesion.estado.writable=False
    form = SQLFORM(db.sesion).process()
    if form.accepted:
        session.flash = "Sesion " + str(form.vars.id)
        asigna_sesion(form.vars.id)
        response.redirect(URL('scan'))
    elif form.errors:
        response.flash = "Por favor verifique los datos introducidos"
    return locals()

@auth.requires(auth.has_membership(role='capturar') or auth.has_membership(role='procesar'))
def setsession():
    rows= db(db.sesion.id>0).select(orderby=~db.sesion.modified_on)
    if request.args(0):
        asigna_sesion(request.args(0,cast=int))
    return locals()

@auth.requires(auth.has_membership(role='capturar'))
def scan():
    if not session.s:
        redirect(URL('sesion'))
    db.barcode.sesion.default = session.s.id
    db.barcode.sesion.writable=False
    db.barcode.sesion.readable=False
    #db.barcode.codigo.requires=[IS_MATCH(e,error_message='Codigo no concuerda con la expresion: '+e)]
    #for e in db.tiposesion(session.s.tiposesion).expresiones:
    e=db.tiposesion(session.s.tiposesion).expresion
    db.barcode.codigo.requires+=[IS_MATCH(e,error_message='Codigo no concuerda con la expresion: '+e)]
    myvar=db.barcode.codigo.requires
    form=SQLFORM(db.barcode).process()
    sesion=session.s
    #form.vars['sesion']= session.sesion
    b1= form.custom.widget.codigo
##    b1.element('input')['_onkeypress']="return focusNext(this.form, 'barcode2', event)"
    b1.element('input')['_autofocus']=''
    b1.element('input')['_autocomplete']='off'
##    b2= form.custom.widget.barcode2
##    b2.element('input')['_autocomplete']='off'
    if form.accepted:
        response.flash='Correcto ' #+ form.vars.codigo
    elif form.errors:
        response.flash='error'

    rows= db(db.barcode.sesion==session.s.id).select('barcode.codigo','barcode.modified_on', orderby=~db.barcode.modified_on, limitby=(0, 5))
    count = db(db.barcode.sesion==session.s.id).count()

    return dict (form=form, rows=rows, sesion=sesion, count=count, myvar=myvar)

def regexhelp():
    return dict()

def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/manage_users (requires membership in
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """
    return dict(form=auth())


@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()


@auth.requires_login() 
def api():
    """
    this is example of API with access control
    WEB2PY provides Hypermedia API (Collection+JSON) Experimental
    """
    from gluon.contrib.hypermedia import Collection
    rules = {
        '<tablename>': {'GET':{},'POST':{},'PUT':{},'DELETE':{}},
        }
    return Collection(db).process(request,response,rules)
