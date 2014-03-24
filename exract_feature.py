from PIL import Image
from pylab import imshow,show,axis,contour,axis, figure,gray,hist
from pylab import array,zeros_like,uint64

# load the image file
img = Image.open('./data/das-0.jpg')
img_gray = img.convert('L')

# create a new figure
figure(); gray(); axis('equal'); axis('off')


imshow(img)
comp_index = []

def flood(img,mask,seed_list,component_dots):
    if not seed_list:
        return
    height,width = img.shape
    next_surround_seed_list = [] 
    component_dots   #[<y,x>,[r,g,b]>, ...]  (n,
    for seed in seed_list:
        y,x=seed
        for delta_y in [-1,0,1]:
            for delta_x in [-1,0,1]:
                y+=delta_y
                x+=delta_x
                if y>height-1:
                    y=height-1
                if y<0:
                    y=0
                if x>width-1:
                    x=width-1
                if x<0:
                    x=0
                if mask[y,x]==0:
                    # check it if it can be merged in this group.
                    dist = linalg.norm(img[y,x]-mean_value) # euclidean distance
                    if dist<10:
                        mask[y,x]=comp_index  
                        next_surround_seed_list.append((y,x))
        
def connected_conponent(img):
    """
    input:  img cant be gray or color. 
            The shape of img is (height,width,..)
    output: list of components  and an image mask
    """
    img.resize((10,10))
    img = array(img)
    assert(img.ndim>=2)
    #mask = array([0]*img.size).reshape(img.shape)
    mask = zeros_like(img,dtype=uint64)  #[h,w]
    comp_list = []
    comp_index = 0   # the index of the first componet  is 1

    print mask.shape, mask.dtype
    print img.shape,img.dtype
    for y in range(img.shape[0]):
        for x in range(img.shape[1]):
            if mask[y,x]==0: # (y,x) will be a seed of component.
                comp_index+=1
                mask[y,x]=comp_index  
                #flood to ne
                flood(img,mask,(y,x))
                
            #print i,j
    #return h


#show()
