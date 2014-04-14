from PIL import Image
from pylab import array,zeros_like,uint64
from pylab import imshow,show,subplot,array,figure,gray,uint8,hist,plot
from pylab import annotate
import numpy as np
import math

def five_points_cross_ratio(point_list):
    """
        input: 5 points.   each point is (Y,X)
        output: 5 cross_ratio

    """
    l = len(point_list)
    assert(l==5)
    cross_ratio_list = []
    for center_point_idx in range(l):
        center_point = point_list[center_point_idx]
        angle_list = []
        for idx in range(l):
            if idx==center_point_idx:
                continue
            p = point_list[idx] 
            angle = math.atan2(p[0]-center_point[0], p[1]-center_point[1])
            angle_list.append(angle)
        assert(len(angle_list)==4)
        #cross_ratio = math.sin(angle_list[2]-angle_list[0])/math.sin(angle_list[2]-angle_list[1])/(math.sin(angle_list[3]-angle_list[0])/math.sin(angle_list[3]-angle_list[1]))
        b = (math.sin(angle_list[2]-angle_list[1])*math.sin(angle_list[3]-angle_list[0]))
        if b==0:
            b=10**(-100)
        cross_ratio = math.sin(angle_list[2]-angle_list[0])*math.sin(angle_list[3]-angle_list[1])/b
        cross_ratio_list.append(cross_ratio)
    return  cross_ratio_list

def sort_by_atan2(point_array,center_point):
    t = sorted(point_array, key=lambda x:math.atan2(x[0]-center_point[0], x[1]-center_point[1]))# (x[0],x[1]) --> (Y,X)
    return np.array(t)

if __name__=='__main__':
    test_sort_by_atan2 = False 
    test_five_points_cross_ratio = True

    if test_sort_by_atan2:
        #p_2d_array=np.array([(4,6),(2,3),(10,4),(8,3),(11,3),(7,4)])
        p_2d_array=np.random.rand(10,2)*10
        center_point = [2,3]
        sorted_array = sort_by_atan2(p_2d_array, center_point)
        print p_2d_array
        print sorted_array 
        figure()
        # plotting the pointlist 
        i=0
        for p in sorted_array:
            i+=1
            annotate('%s'%i, xy=(p[1],p[0]),   xytext=(p[1]+0.1,p[0]+0.1))
            #annotate('%s'%i, xy=(p[1],p[0]),   xytext=(p[1]+0.5,p[0]+1),arrowprops=dict(facecolor='black'))
        plot(p_2d_array[:,1],p_2d_array[:,0],'ob',center_point[1],center_point[0],'or')
        # highlighting the neighbours
        #plot(p_2d_array[neig_idx,1],p_2d_array[neig_idx,0],'o', markerfacecolor='None',markersize=15,markeredgewidth=1)
        show()

    if test_five_points_cross_ratio:
        #p_2d_array=np.random.rand(5,2)*10
        p_2d_array=np.array([(4,6),(2,3),(10,4),(11,3),(7,4)])
        cross_ratio_list = five_points_cross_ratio(p_2d_array)
        print cross_ratio_list 

        # check different sorted sequece has different ratios
        p_2d_array=np.array([(2,3),(4,6),(10,4),(11,3),(7,4)])
        cross_ratio_list = five_points_cross_ratio(p_2d_array)
        print cross_ratio_list 
