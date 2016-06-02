# -*- coding: utf-8 -*-

db.define_table('container',
                Field('barcode','string',length=100,notnull=True,unique=True,requires=[IS_NOT_EMPTY(),IS_LENGTH(18)]),
                auth.signature, format='%(barcode)s')

db.define_table('impreso',
                Field('record','text'),
                Field('barcode','string',length=100,notnull=True,unique=True),
                Field('segment','string'),
                Field('consecutive','integer'))

db.define_table('pieza',
                Field('barcode1','string',length=100,notnull=True,unique=True,requires=[IS_NOT_EMPTY(),IS_NOT_IN_DB(db,'pieza.barcode1'),IS_LENGTH(10)]),
                Field('barcode2','string',length=100,notnull=True,unique=True,requires=[IS_NOT_EMPTY(),IS_NOT_IN_DB(db,'pieza.barcode2'),IS_LENGTH(18)]),
                Field('container','reference container'),
                auth.signature)


def validate_pieza_form(form):
    exists = db(db.impreso.barcode==form.vars.barcode1).select().first()
    if not exists:
        form.errors.barcode1='Codigo no valido'
    exists2 = db(db.container.barcode==form.vars.barcode2).select().first()
    if exists2:
        form.errors.barcode2='Codigo ya escaneado en caja ' + exists2.barcode


def validate_container_form(form):
    exists = db(db.pieza.barcode2==form.vars.barcode).select().first()
    if exists:
        form.errors.barcode='Codigo ya escaneado en pieza ' + exists.barcode2
    exists2 = db(db.impreso.barcode==form.vars.barcode).select().first()
    if exists2:
        form.errors.barcode='Codigo no valido para caja ' + exists2.barcode
