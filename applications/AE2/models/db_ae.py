# -*- coding: utf-8 -*-
db.define_table('job',Field('nombre', requires=IS_NOT_EMPTY()),
                   Field('separador_reg'),
                   Field('separador_men'),
                   Field('comentario','text'),
                   Field('tasks','list:reference scheduler_task', default =[]),
                   auth.signature,
                   format='(%(id)d) %(nombre)s')

#bd
#Agencia,Comunicación,Num Cte,Paterno,Materno,Nombre,Marca,Modelo,Sexo,
#Calle,C.P.  Cte,Col. Cte,Mpio. Cte,Edo. Cte,Ciudad Cte,ID QUEJA,FOLIO,
#Director Marca,Gte. General,Segmentos Inserto

db.define_table('registro',Field('agencia'),
                         Field('comunicacion'),
                         Field('numcte'),
                         Field('paterno'),
                         Field('materno'),
                         Field('nombre'),
                         Field('marca'),
                         Field('modelo'),
                         Field('sexo'),
                         Field('calle'),
                         Field('cp'),
                         Field('col'),
                         Field('mpio'),
                         Field('edo'),
                         Field('ciudad'),
                         Field('idqueja'),
                         Field('folio',requires=IS_NOT_IN_DB(db,'db.registros')),
                         Field('directormarca'),
                         Field('gtegeneral'),
                         Field('segmentosinserto'),
                         Field('seq','integer'),
                         Field('comms','list:string'),
                         Field('job','reference job'))
#archivo de mensajes
def clasifica(r):
    d = r['descripcion'].upper()
    if d:
        if 'BIENVENIDA' in d:
            return '10-BIENVENIDA'
        elif 'CUMPLEA' in d:
            return '30-ANIVERSARIO'
        elif 'DESPEDIDA' in d:
            return '40-DESPEDIDA'
        else:
            return '20-CUERPO'
    return

db.define_table('mensaje',Field('descripcion',requires=IS_NOT_EMPTY()),
                          Field('texto','text',requires=IS_NOT_EMPTY()),
                          Field('typecode', compute = lambda r: clasifica(r)),
                          Field('job','reference job'),
                          format='%(descripcion)s')

db.define_table('comunicacion',Field('nombre',requires=IS_NOT_EMPTY()),
                               Field('frecuencia','integer'),
                               Field('job','reference job'),
                               format='%(nombre)s')

db.define_table('comunicacion_y_mensaje',Field('condicional','boolean',default=False),
                                         Field('condicion'),
                                         Field('comunicacion','reference comunicacion'),
                                         Field('mensaje','reference mensaje'),
                                         auth.signature)

if not (db(db.auth_group.role=='administradores').select()):
    db.auth_group.insert(role='administradores')
