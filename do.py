from PIL import Image
from pylab import imshow,show,subplot,array,figure,gray,uint8,hist
import numpy as np
from pylab import jet

from skimage import filter
from scipy.ndimage import filters,measurements
from scipy import stats

if __name__=="__main__":
    #file_name='./data/das-0.jpg'
    #file_name='./data/EngBill21.jpg'
    #file_name='./data/sample1.jpg'
    file_name='/Users/xcbfreedom/projects/data/formula_images/user_images/531283fa24f0b8afb.png'
    # load the image file
    img = Image.open(file_name)
    print img

    #======= find word regions ========
    # convert to gray
    img_gray = array(img.convert('L'))   # not inplace operator
    img_gray = 255-img_gray

    # binary
    #img_bin = filter.threshold_adaptive(img_gray,17,method='mean')
    global_thresh = filter.threshold_otsu(img_gray)
    img_bin = img_gray > global_thresh 

    # find connect components 
    s = array([[1,1,1],[1,1,1],[1,1,1]])

    # the mask image and num of objects
    labeled_array, num_features = measurements.label(img_bin, structure=s)
    print 'num of labels:', num_features 


    ob_area_list = []
    #for ob in obj_list:
    #h = ob[0].stop-ob[0].start
    #w = ob[1].stop-ob[1].start
    #print ob, h, w
    img_bin_words = np.zeros_like(img_bin)
    word_label_list = []
    for i in range(num_features):
        mask_value=i+1
        area = measurements.sum(img_bin,labeled_array,index=mask_value)
        if area<20:
            continue
        print area
        ob_area_list.append(area)
        word_label_list.append(mask_value)
        img_bin_words[labeled_array==mask_value]=img_bin[labeled_array==mask_value]
    #hist(ob_area_list)
    area_mode = stats.mode(ob_area_list,axis=None)
    print area_mode

    #print img_bin,stats.mode(img_bin,axis=None)
    #print img_bin,np.max(img_bin)

    # do gaussian blur to the bin img
    #img_bin = filters.gaussian_filter(img_bin,0.26935)
    #print img_bin,stats.mode(img_bin,axis=None)
    #print img_bin,np.max(img_bin)

    # binary again
    #img_bin = filters.maximum_filter(img_bin,7)
    #img_bin = filter.threshold_adaptive(img_bin,7)

    #img_bin[img_bin>0]=255
    #Image.fromarray(uint8(img_bin)).save('feature_points.png')

    #====== extract the centroids of word regions=====  
    # list of slice index of object's box
    obj_list = measurements.find_objects(labeled_array)
    print 'num of objs:', len(obj_list) 
    print 'num of words:', len(word_label_list)
    for i in word_label_list:
        word = obj_list[i-1]
        y = (word[0].stop-word[0].start)/2 
        x = (word[1].stop-word[1].start)/2 
        print x,y

    figure(); gray(); # don't use colors 

    # show the two pics  on 1*2 frame
    #subplot(1,3,1)   
    imshow(img_gray)
    #subplot(1,3,2)
    figure(); gray(); # don't use colors 
    imshow(img_bin)
    figure(); gray(); # don't use colors 
    imshow(img_bin_words)
    #subplot(1,3,3)
    #imshow(labeled_array)
    #ob = labeled_array[obj_list[100]]
    figure(); gray(); # don't use colors 
    imshow(labeled_array)

    # starts the figure GUI and raises the figure windows

    jet()
    show()
