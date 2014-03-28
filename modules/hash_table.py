#!/usr/bin/env python
# -*- coding:utf-8 -*-
from PIL import Image
from pylab import array,zeros_like,uint64
from pylab import imshow,show,subplot,array,figure,gray,uint8,hist,plot
from pylab import annotate
import numpy as np
import math

import sys  
sys.path.append('/Users/xcbfreedom/projects/web2py/web2py.app/Contents/Resources/')   

from gluon.dal import DAL,Field
from gluon.sqlhtml import SQLFORM
from gluon.validators import IS_NOT_EMPTY, IS_EMAIL, IS_LENGTH,IS_IN_DB


db = DAL("sqlite://mydb.sqlite")
db.define_table('t_doc_image',
        Field('title', 'string',unique=True),
        Field('internal_filename', 'upload'),
        format = '%(title)s')

db.define_table('t_point_pattern',
        Field('hash_index', 'double'),
        Field('doc_id', 'reference t_doc_image'),
        Field('point_id', 'integer'),
        Field('pattern_id', 'integer'),
        format = '%(hash_index)s-%(doc_id)s-%(point_id)s-%(pattern_id)s')

db.t_point_pattern.doc_id.requires = IS_IN_DB(db, db.t_doc_image.id, '%(title)s')
 
db.t_point_pattern.doc_id.writable = db.t_point_pattern.doc_id.readable = False


document_total_num = 1000

firt_voting_table=np.zeros(document_total_num,dtype=np.int)
second_voting_table=np.zeros(document_total_num,dtype=np.int)

hash_table = []
def register_to_hashtable(Document_ID, Point_ID, nCm_Pattern_ID, H_index):
    """
        input: 5 points.   each point is (Y,X)
        output: 5 cross_ratio

    """
    nCm_pattern = (Document_ID, Point_ID, nCm_Pattern_ID, H_index)
    hash_table.append(nCm_pattern)
    print 'register:',nCm_pattern
    print 'total:', len(hash_table)
    print 'unique:', len(set(hash_table))


def lookup_hashtable(Document_ID, Point_ID, nCm_Pattern_ID, H_index):
    nCm_pattern = (Document_ID, Point_ID, nCm_Pattern_ID, H_index)
    #print 'lookup:',nCm_pattern
    return [{'doc_id':123,'point_id':100},{'doc_id':11,'point_id':100}]


def first_vote_by_hashtable(Document_ID, Point_ID, nCm_Pattern_ID, H_index):
    global firt_voting_table
    global second_voting_table
    cell_list = lookup_hashtable(Document_ID, Point_ID, nCm_Pattern_ID, H_index)
    for cell in cell_list:
        firt_voting_table[cell['doc_id']] +=1


def get_topk_in_second_vote_table(k=1):
    """
    """
    t = sorted(second_voting_table,reverse=True)
    return t[:k]

def summary_first_vote(): 
    threshold_l=0.5
    global firt_voting_table
    global second_voting_table
    for i in firt_voting_table:
        if firt_voting_table[i]>threshold_l:
            second_voting_table[i]+=1 
    print 'summary_first_vote',firt_voting_table
    #clear the first voting table
    firt_voting_table *=0

