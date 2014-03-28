#!/usr/bin/env python
# -*- coding:utf-8 -*-
from PIL import Image
from pylab import array,zeros_like,uint64
from pylab import imshow,show,subplot,array,figure,gray,uint8,hist,plot
from pylab import annotate
import numpy as np
import math


class HashTable(object):
    vote_table_size = 1000
    firt_voting_table=np.zeros(vote_table_size,dtype=np.int)
    second_voting_table=np.zeros(vote_table_size,dtype=np.int)
    def __init__(self):
        pass

    def insert(self, nCm_pattern):
        """
            to database
            input: (Document_ID, Point_ID, nCm_Pattern_ID, H_index)
            output:
        """
        raise NotImplementedError("Please Implement this method")

    def select(self, H_index):
        """
            from database
            input: hash value
            output: [{'doc_id':123,'point_id':100},{'doc_id':11,'point_id':100}]
        """
        raise NotImplementedError("Please Implement this method")

    def register_to_hashtable(self,Document_ID, Point_ID, nCm_Pattern_ID, H_index):
        """
            input: 5 points.   each point is (Y,X)
            output: 5 cross_ratio

        """
        nCm_pattern = (Document_ID, Point_ID, nCm_Pattern_ID, H_index)
        self.insert(nCm_pattern)
        print 'register:',nCm_pattern
        #print 'total:', len(hash_table)
        #print 'unique:', len(set(hash_table))


    def first_vote_by_hashtable(self, H_index):
        #print 'to find hash:',H_index
        cell_list = self.select(H_index)
        #print 'found cell_list:',cell_list
        #return [{'doc_id':123,'point_id':100},{'doc_id':11,'point_id':100}]
        for cell in cell_list:
            HashTable.firt_voting_table[cell['doc_id']] +=1


    def get_topk_in_second_vote_table(self, k=10):
        """
            topk matched image id
            input: k
            ouput: [(top1_index, match_value),(top2_idx, match_value),...]
        """
        t = HashTable.second_voting_table
        tmp = zip(range(len(t)),t)
        top_list = sorted(tmp,key=lambda x:x[1],reverse=True)
        return top_list[:k]

    def summary_first_vote(self): 
        """
        complete all 5 points combinations from one nCm for the centrial piont
            
        """
        threshold_l=0.5
        for i in HashTable.firt_voting_table:
            if HashTable.firt_voting_table[i]>threshold_l:
                HashTable.second_voting_table[i]+=1 
        print 'summary_first_vote',HashTable.firt_voting_table
        #clear the first voting table
        HashTable.firt_voting_table *=0

if __name__=="__main__":
    pass
