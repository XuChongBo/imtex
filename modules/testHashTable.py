#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys  
sys.path.append('/Users/xcbfreedom/projects/web2py/web2py.app/Contents/Resources/')   
from gluon.dal import DAL, Field
from gluon.sqlhtml import SQLFORM
from gluon.validators import IS_NOT_EMPTY, IS_EMAIL, IS_LENGTH,IS_IN_DB
from hash_table import HashTable

class TestTable(HashTable):
    def __init__(self):
        from testdb import db
        self.db = db

    def insert(self,nCm_pattern):
        """
            to database
            input: (Document_ID, Point_ID, nCm_Pattern_ID, H_index)
            output:
        """
        Document_ID, Point_ID, nCm_Pattern_ID, H_index=nCm_pattern
        self.db.t_point_pattern.insert(hash_index=H_index,doc_id=Document_ID,point_id=Point_ID, pattern_id=nCm_Pattern_ID)
        self.db.commit()

    def select(self, H_index):
        """
            from database
            input: hash value
            output: [{'doc_id':123,'point_id':100},{'doc_id':11,'point_id':100}]
        """
        rows = self.db(self.db.t_point_pattern.hash_index==H_index).select()
        res = []
        for r in rows:
            res.append({'doc_id':r.doc_id,'point_id':r.point_id})  
        return res

