from PIL import Image
from pylab import imshow,show,axis,array,zeros,imsave,imread
import numpy as np
import os
import cStringIO
from gluon import current

def resize_image():
    db = current.globalenv['db']
    rows = db(db.t_doc_image.id==current.request.args[0]).select()
    f = rows.first().file
    f = os.path.join(current.request.folder,'uploads',f) 
    print f
    im3 = Image.open(f)
    im3 = im3.resize((550,100))
    im3 = im3.rotate(45)
    stream=cStringIO.StringIO()
    imsave(stream,np.array(im3))
    return stream.getvalue()
