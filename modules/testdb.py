#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys  
sys.path.append('/Users/xcbfreedom/projects/web2py/web2py.app/Contents/Resources/')   
from gluon.dal import DAL, Field
from gluon.sqlhtml import SQLFORM
from gluon.validators import IS_NOT_EMPTY, IS_EMAIL, IS_LENGTH,IS_IN_DB

db = DAL("sqlite://data/mydb.sqlite")
db.define_table('t_doc_image',
        Field('title', 'string',unique=True),
        Field('internal_filename', 'upload'),
        format = '%(title)s')

db.define_table('t_point_pattern',
        Field('hash_index', 'integer'),
        Field('doc_id', 'reference t_doc_image'),
        Field('point_id', 'integer'),
        Field('pattern_id', 'integer'),
        format = '%(hash_index)s-%(doc_id)s-%(point_id)s-%(pattern_id)s')

db.t_point_pattern.doc_id.requires = IS_IN_DB(db, db.t_doc_image.id, '%(title)s')
 
db.t_point_pattern.doc_id.writable = db.t_point_pattern.doc_id.readable = False

if __name__=="__main__":
    db.t_doc_image.insert(title='title2',internal_filename='filenamex')
    #db.t_point_pattern.insert(hash_index=456,doc_id=2,point_id=0, pattern_id=0)

    db.commit()

    #print db(db.t_point_pattern.hash_index==H_index).select()

    print db(db.t_doc_image).select()
    print db(db.t_point_pattern).select()
