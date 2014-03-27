from PIL import Image
from pylab import imshow,show,subplot,array,figure,gray,uint8,hist,plot
import numpy as np
from pylab import jet,annotate

import itertools

from skimage import filter
from scipy.ndimage import filters,measurements
from scipy import stats
from knn_search import knn_search
from feature_extract import sort_by_atan2
from feature_extract import five_points_cross_ratio
from db import register_to_hashtable
#showFigure=True
showFigure=False

def find_nearest_points(p_2d_array,p_idx, N=8):
    p=p_2d_array[p_idx]
    # performing the search
    neighbours_idx = knn_search(p_idx,p_2d_array,N)
    if showFigure:
        figure()
        imshow(img)
        # plotting the pointlist and the query point
        plot(p_2d_array[:,1],p_2d_array[:,0],'ob',p[1],p[0],'or')

        # highlighting the neighbours
        plot(p_2d_array[neighbours_idx,1],p_2d_array[neighbours_idx,0],'o', markerfacecolor='None',markersize=15,markeredgewidth=1)
        show()
    
    nearest_n_points = p_2d_array[neighbours_idx]
    
    print 'center point:', p
    #print 'nearest_n_points:', nearest_n_points
    # sort by atan2.  center on p. 
    nearest_n_points = sort_by_atan2(nearest_n_points,p)
    #print 'nearest_n_points sorted:', nearest_n_points
    return nearest_n_points  

def get_word_centroid_points(img):
    """
        find the connected component who's area satisfy some condition, which can be identified to be word regions.
        
        input: img
        output:
             (word_centroid_y_list,word_centroid_x_list)
    """
    #==== preprocess 
    # convert to gray
    img_gray = array(img.convert('L'))   # not inplace operator
    img_gray = 255-img_gray

    if showFigure:
        figure(); gray(); # don't use colors 
        imshow(img_gray)
        show()
    # binary
    #img_bin = filter.threshold_adaptive(img_gray,17,method='mean')
    global_thresh = filter.threshold_otsu(img_gray)
    img_bin = img_gray > global_thresh 

    if showFigure:
        figure(); gray(); # don't use colors 
        imshow(img_bin)
        show()

    #== find connect components 
    s = array([[1,1,1],[1,1,1],[1,1,1]])
    # the mask image and num of objects
    labeled_array, num_features = measurements.label(img_bin, structure=s)
    print 'num of labels:', num_features 
    if showFigure:
        figure(); gray(); # don't use colors 
        imshow(labeled_array)
        jet()
        show()
    
    #== filter the connected component by area
    word_area_list = []
    word_label_array = np.zeros_like(labeled_array)
    word_label_list = []
    for i in range(num_features):
        mask_value=i+1
        area = measurements.sum(img_bin,labeled_array,index=mask_value)
        if area<20:
            continue
        print area
        word_area_list.append(area)
        word_label_list.append(mask_value)
        word_label_array[labeled_array==mask_value]=labeled_array[labeled_array==mask_value]
    #hist(word_area_list)
    area_mode = stats.mode(word_area_list,axis=None)
    print area_mode

    if showFigure:
        figure(); gray(); # don't use colors 
        imshow(word_label_array)
        jet()
        show()
    #print img_bin,stats.mode(img_bin,axis=None)
    #print img_bin,np.max(img_bin)

    # do gaussian blur to the bin img
    #img_bin = filters.gaussian_filter(img_bin,0.26935)
    #print img_bin,stats.mode(img_bin,axis=None)
    #print img_bin,np.max(img_bin)

    # binary again
    #img_bin = filters.maximum_filter(img_bin,7)
    #img_bin = filter.threshold_adaptive(img_bin,7)

    # === list of slice index of object's box
    obj_list = measurements.find_objects(word_label_array)
    print 'num of objs:', len(obj_list) 
    print 'num of words:', len(word_label_list)
    word_centroid_y_list =[]
    word_centroid_x_list =[]
    for i in word_label_list:
        word = obj_list[i-1]
        y = (word[0].stop+word[0].start)/2 
        x = (word[1].stop+word[1].start)/2 

        word_centroid_y_list.append(y)
        word_centroid_x_list.append(x)
        #print x,y

        #h = ob[0].stop-ob[0].start
        #w = ob[1].stop-ob[1].start
        #print ob, h, w
    return (word_centroid_y_list, word_centroid_x_list)

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

    #====== extract word regions and their centroids=====  
    y_list, x_list = get_word_centroid_points(img)

    figure(); 
    imshow(img)
    plot(x_list,y_list,'r*')
    show()
