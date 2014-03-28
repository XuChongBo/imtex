import numpy as np
from pylab import plot,show
from pylab import imshow,show,axis,contour,axis, figure,gray,hist,ion
from scipy.spatial.distance import euclidean 

def caculate_dist_matrix(point_2d_array):
    l = len(point_2d_array)
    m = np.zeros((l,l),dtype=np.float)
    for i in range(l-1):
        for j in range(i+1,l):
            #http://docs.scipy.org/doc/scipy/reference/generated/scipy.spatial.distance.euclidean.html
            d = euclidean(point_2d_array[i],point_2d_array[j])
            m[i,j]=d
            m[j,i]=d
    return m

#dist_matrix = None
def knn_search(p_idx, point_2d_array, K):
    """ 
        find K nearest neighbours of the point with index p_idx  in point list
        return the neighgbours' index list
    """
    #global dist_matrix
    #if dist_matrix is None:
    dist_matrix = caculate_dist_matrix(point_2d_array)
    l = len(point_2d_array)
    K = K if K < l else l

    # get euclidean distances from the other points
    dist_list = dist_matrix[p_idx]

    # sorting
    sorted_idx = np.argsort(dist_list) 
    # return the indexes of K nearest neighbours
    return sorted_idx[1:K+1]

if __name__=='__main__':
    p_2d_array=np.array([(4,6),(2,3),(10,4),(8,3),(11,3),(7,4)])
    m = caculate_dist_matrix(p_2d_array)
    print p_2d_array
    print m

    p_idx =4 
    x=p_2d_array[p_idx]
    # performing the search
    neig_idx = knn_search(p_idx,p_2d_array,3)
    figure()

    # plotting the pointlist and the query point
    plot(p_2d_array[:,1],p_2d_array[:,0],'ob',x[1],x[0],'or')

    # highlighting the neighbours
    plot(p_2d_array[neig_idx,1],p_2d_array[neig_idx,0],'o', markerfacecolor='None',markersize=15,markeredgewidth=1)
    show()
