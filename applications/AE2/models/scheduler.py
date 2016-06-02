# -*- coding: utf-8 -*-
from os import path

def __populate_comunicado_for_job(jobid):
    db(db.comunicacion.job==jobid).delete()
    count = db.registro.comunicacion.count()
    rows = db(db.registro.job==jobid).select(
                                              db.registro.comunicacion,
                                              count,
                                              groupby=db.registro.comunicacion,
                                              orderby=~count)
    db.comunicacion.job.default = jobid
    for r in rows:
        db.comunicacion.update_or_insert(
                                          (db.comunicacion.job==jobid) & 
                                          (db.comunicacion.nombre == r.registro.comunicacion),
                                          nombre=r.registro.comunicacion,frecuencia=r[count])
    return

def upload_file(jobid,tablename,csvfile):
    db[tablename].job.default=jobid
    fullname=path.join(db._adapter.folder, '..', 'uploads',csvfile)
    db[tablename].import_from_csv_file(open(fullname,'r'))
    db.commit()
    __populate_comunicado_for_job(jobid)
    db.commit()
    

from gluon.scheduler import Scheduler
scheduler = Scheduler(db)
