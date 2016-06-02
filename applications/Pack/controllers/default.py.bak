# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a sample controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
## - api is an example of Hypermedia API support and access control
#########################################################################

def index():
    if not session.current_container :
        redirect(URL('setcontainer'))
    else:
        redirect(URL('scanpieza'))

def setcontainer():
    form = SQLFORM.factory(
        Field('containercode', requires=[IS_NOT_EMPTY(),IS_NOT_IN_DB(db,'impreso.barcode')],label='Codigo de Caja'))
    b= form.custom.widget.containercode
    b.element('input')['_autocomplete']='off'
    b.element('input')['_autofocus']=''

    if form.process().accepted:
        # cid = db.container(id,barcode=form.vars.containercode)
        cid = db(db.container.barcode==form.vars.containercode).select().first()
        #return form.vars.containercode + str(cid.id) + cid.barcode
        #record = db.mytable(id,myfield='somevalue')
        if not cid:
            cid = db.container.insert(barcode=form.vars.containercode)
        session.current_container = form.vars.containercode
        session.cid= cid.id
        session.flash = 'Contenedor Actual:' + form.vars.containercode
        redirect(URL('scanpieza',args=cid.id))
    elif form.errors:
        response.flash = 'la forma tiene errores'
    return dict(form=form)

def scanpieza():
    container = db.container[session.cid]
    if container:
        db.pieza.container.default=container.id
        db.pieza.container.writable=False

        form=SQLFORM(db.pieza).process(onvalidation=validate_pieza_form)
        b1= form.custom.widget.barcode1
        b1.element('input')['_onkeypress']="return focusNext(this.form, 'barcode2', event)"
        b1.element('input')['_autofocus']=''
        b1.element('input')['_autocomplete']='off'
        b2= form.custom.widget.barcode2
        b2.element('input')['_autocomplete']='off'
        if form.accepted:
            response.flash='Correcto ' + container.barcode + ' ' +  form.vars.barcode1 + ' ' + form.vars.barcode2
        elif form.errors:
            response.flash='error'
        return dict (form=form)
    else:
        redirect(URL('setcontainer'))

def piezas():
    db.pieza.id.readable=False 
    db.pieza.modified_on.readable= True
    query=((db.pieza.id > 0))

    fields = (db.pieza.id, db.pieza.container, db.pieza.barcode1, db.pieza.barcode2, db.pieza.modified_on)

    #Define headers as tuples/dictionaries
    headers = {'pieza.id':   'ID',
           'pieza.container': 'Caja',
           'pieza.barcode1': 'Acuse',
           'pieza.barcode2': 'codigo externo',
           'pieza.modified_on': 'Fecha y Hora'
           }

    #Let's specify a default sort order on date_of_birth column in grid
    default_sort_order=[~db.pieza.modified_on]

    #Creating the grid object
    form = SQLFORM.grid(query=query, fields=fields, headers=headers, orderby=default_sort_order,
                create=False, deletable=False, editable=False, maxtextlength=64, paginate=25)

    return dict(form=form)

def container_detail():
    db.pieza.id.readable=False
    db.pieza.modified_on.readable= True
    if session.cid:
        query=((db.pieza.container == session.cid))
    else:
        redirect(URL('setcontainer'))

    fields = (db.pieza.id, db.pieza.container, db.pieza.barcode1, db.pieza.barcode2, db.pieza.modified_on)

    #Define headers as tuples/dictionaries
    headers = {'pieza.id':   'ID',
           'pieza.container': 'Caja',
           'pieza.barcode1': 'Acuse',
           'pieza.barcode2': 'codigo externo',
           'pieza.modified_on': 'Fecha y Hora'
           }

    #Let's specify a default sort order on date_of_birth column in grid
    default_sort_order=[db.pieza.modified_on]

    #Creating the grid object
    form = SQLFORM.grid(query=query, fields=fields, headers=headers, orderby=default_sort_order,
                create=False, deletable=False, editable=False, maxtextlength=64, paginate=25)

    return dict(form=form)



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
