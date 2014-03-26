from PIL import Image
from pylab import array,zeros_like,uint64
from pylab import imshow,show,subplot,array,figure,gray,uint8,hist,plot
from pylab import annotate
import numpy as np
import math

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

