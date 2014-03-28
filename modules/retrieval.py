from PIL import Image
from pylab import imshow,show,subplot,array,figure,gray,uint8,hist,plot
import numpy as np
from pylab import jet,annotate
import time

import itertools

from skimage import filter
from scipy.ndimage import filters,measurements
from scipy import stats
from knn_search import knn_search
from feature_extract import sort_by_atan2
from feature_extract import five_points_cross_ratio
from hash_table import register_to_hashtable,lookup_hashtable,first_vote_by_hashtable,get_topk_in_second_vote_table,summary_first_vote
from word_region_identify import get_word_centroid_points,find_nearest_points

#showFigure=True
showFigure=False

def image_retrieval(img):
    """
        1.find word point in img 
        2.caculate the point features
        3.use the point features to retrieval the similar images

        input: PIL img
        output: image_id_list
    """

    #====== extract word regions and their centroids=====  
    y_list, x_list = get_word_centroid_points(img)

    figure(); 
    imshow(img)
    plot(x_list,y_list,'r*')
    show()
    start_time = time.time()
    p_2d_array=np.array(zip(y_list,x_list))
    word_point_num = len(p_2d_array)
    print 'word_point_num:', word_point_num

    for p_idx in range(word_point_num):
        Point_ID = p_idx
        nearest_points = find_nearest_points(p_2d_array,p_idx, N=8)
        #print nearest_points
        if showFigure:
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

            show()

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
                    first_vote_by_hashtable(Document_ID, Point_ID, nCm_Pattern_ID, H_index)
                    mC5_Pattern_ID += 1 
                    
                #Increment the cell of the second voting table if the document ID in the first voting table has votes larger than the threshold l.
                #clear the first voting table.
                summary_first_vote()
            #break #nCm_pattern
            nCm_Pattern_ID += 1
        #break #all point
    #Return document id which has the largest votes in the second voting table
    print 'the result doc_id:', get_topk_in_second_vote_table()

    end_time = time.time()
    print " cost:%s s" % int(end_time-start_time)

if __name__=="__main__":
    #file_name='./data/das-0.jpg'
    #file_name='./data/EngBill21.jpg'
    #file_name='./data/sample1.jpg'
    file_name='/Users/xcbfreedom/projects/data/formula_images/user_images/531283fa24f0b8afb.png'
    Document_ID = file_name
    # load the image file
    img = Image.open(file_name)

    if showFigure:
        figure(); 
        imshow(img)
        show()

    image_retrieval(img)
