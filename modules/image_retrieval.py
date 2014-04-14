from PIL import Image
import matplotlib
matplotlib.use('Agg')
from pylab import imshow,subplot,array,figure,gray,uint8,hist,plot
import numpy as np
from pylab import jet,annotate
import time
import output_the_plot

import itertools

from skimage import filter
from scipy.ndimage import filters,measurements
from scipy import stats
from knn_search import knn_search
from feature_extract import sort_by_atan2
from feature_extract import five_points_cross_ratio
from word_region_identify import get_word_centroid_points,find_nearest_points

toPlot=True
#toPlot=False

hash_table = None

def image_retrieval(img):
    """
        1.find word point in img 
        2.caculate the point features
        3.use the point features to retrieval the similar images

        input: PIL img
        output: image_id_list
    """
    Document_ID = 'ToSearch'
    #====== extract word regions and their centroids=====  
    y_list, x_list = get_word_centroid_points(img,Document_ID)

    if toPlot:
        figure(); 
        imshow(img)
        plot(x_list,y_list,'r*')
        output_the_plot.output('word_points_%s.png' % Document_ID)

    start_time = time.time()
    p_2d_array=np.array(zip(y_list,x_list))
    word_point_num = len(p_2d_array)
    print 'word_point_num:', word_point_num

    for p_idx in range(word_point_num):
        Point_ID = p_idx
        nearest_points = find_nearest_points(p_2d_array,p_idx, N=8)
        #print nearest_points
        if toPlot:
            figure()
            imshow(img)
            center_point = p_2d_array[p_idx]

            #annotate the neighbours
            i=0
            for p in nearest_points:
                i+=1
                annotate('%s'%i, xy=(p[1],p[0]),   xytext=(p[1]+5,p[0]+5))
            plot(p_2d_array[:,1],p_2d_array[:,0],'ob',center_point[1],center_point[0],'or')
 
            # highlighting the neighbours
            plot(nearest_points[:,1],nearest_points[:,0],'o', markerfacecolor='None',markersize=15,markeredgewidth=1)

            output_the_plot.output('knn_per_point_%s_%s.png' % (p_idx,Document_ID))

        #All m points combinations from Pn
        m=7
        nCm_list = itertools.combinations(nearest_points, m)
        nCm_Pattern_ID = 0
        for nCm in nCm_list:
            print  nCm   

            #get Cyclic permutations of nCm
            for start_i in range(m):
                cyclic_idx = np.arange(start_i,start_i+m)%m
                cyc_nCm = np.array(nCm)[cyclic_idx] 
                print 'cyc_nCm:',cyc_nCm
                #get All 5 points combinations from nCm
                mC5_pattern_list = itertools.combinations(cyc_nCm, 5)
                mC5_Pattern_ID = 0
                for mC5 in mC5_pattern_list:
                    print mC5 
                    cross_ratio_list = five_points_cross_ratio(mC5)
                    Vmax = 10    #the maximum value of the possible discrete cross-ratios
                    pat = mC5_Pattern_ID 
                    H_index = 0
                    cr_i = 0
                    for cr in cross_ratio_list:
                        H_index= cr * ( (Vmax+1)**cr_i )
                        cr_i +=1
                    H_index += pat* ((Vmax+1)**5)

                    #Look up the hash table using H_index and increment the corresponding cell of the first voting table.
                    hash_table.first_vote_by_hashtable(H_index)
                    mC5_Pattern_ID += 1 
                    
                #Increment the cell of the second voting table if the document ID in the first voting table has votes larger than the threshold l.
                #clear the first voting table.
                hash_table.summary_first_vote()
            #break #nCm_pattern
            nCm_Pattern_ID += 1
        #break #all point
    #Return document id which has the largest votes in the second voting table
    match_doc_list = hash_table.get_topk_in_second_vote_table()
    print 'the result (doc_id,match_value) list:', match_doc_list

    end_time = time.time()
    time_cost = int(end_time-start_time)
    print " cost:%s s" % time_cost
    return (match_doc_list, time_cost)

if __name__=="__main__":
    #file_name='./data/das-0.jpg'
    #file_name='./data/EngBill21.jpg'
    #file_name='./data/sample1.jpg'
    file_name='/Users/xcbfreedom/projects/data/formula_images/user_images/531283fa24f0b8afb.png'
    # load the image file
    img = Image.open(file_name)

    if toPlot:
        figure(); 
        imshow(img)
        output_the_plot.output('test.png')

    from testHashTable import TestTable
    hash_table = TestTable()
    image_retrieval(img)
