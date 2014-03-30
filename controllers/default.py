from PIL import Image
import os
import traceback
import gluon.contrib.simplejson as json
import fnmatch

def index():
    return dict(url_show_all_images=URL('show_all_images'))

    #URL('retrieval')

def show_all_images():
    form = SQLFORM(db.t_doc_image)
    if form.accepts(request,session):
        response.flash = 'Thanks! The form has been submitted.'
        #accepted values
        #uploaded_image_record = db(db.t_doc_image.id==form.vars.id).select()
        #print uploaded_image_record
    elif form.errors:
        response.flash = 'Please correct the error(s).'
    image_records = db().select(db.t_doc_image.ALL)
    hash_index_count = db(db.t_point_pattern).count(distinct=db.t_point_pattern.hash_index)
    total_count = db(db.t_point_pattern).count()
    #return dict(form=form, records=image_records)
    return locals()

def feature_view_div():
    img_id = request.args[0]
    return locals()

def feature_caculate_div():
    img_id = request.args[0]
    bin_img_file =os.path.join(request.folder,'uploads','binary_%s.png' % img_id)
    caculateDone = os.path.isfile(bin_img_file)
    return locals()

def remove_the_register():
    try:
        print "in remove_the_register"
        img_id = request.args[0]
        db(db.t_point_pattern.doc_id==img_id).delete()
    except:
        print traceback.format_exc()
        js_rt = "alert(JSON.stringify('%s'));"  % json.dumps(traceback.format_exc())

    return js_rt+"window.location.reload();"
    #return "alert('xx');jQuery('#caculate_div_%s').load('%s');" % (img_id,URL('feature_caculate_div',args=[1]))

def image_register():
    try:
        print "in image_register"
        img_id = request.args[0]
        import image_register as img_register
        img_register.hash_table =MyHashTable(db) 
        bin_img_file =os.path.join(request.folder,'uploads','binary_%s.png' % img_id)

        if not os.path.isfile(bin_img_file):
            img_record = db.t_doc_image(id=img_id)
            f = img_record.internal_filename
            f = os.path.join(request.folder,'uploads',f)
            img = Image.open(f)
            img_register.image_register(img,img_id)
    except:
        print traceback.format_exc()
        db.rollback()
        js_rt = "alert(JSON.stringify('%s'));"  % json.dumps(traceback.format_exc())
        
    return js_rt+"window.location.reload();"
    #return "jQuery('#caculate_div_2').html('<h2>abc</h2>');"
    #return "jQuery('#caculate_div_%s').load('%s');" % (img_id,URL('feature_caculate_div',args=[1]))

def caculate_detail():
    doc_id = request.args[0]
    path=os.path.join(request.folder,'uploads')
    knn_per_point_image_list = [f for f in os.listdir(path) if fnmatch.fnmatch(f, 'knn_per_point_%s_*.png' % doc_id)]
    print knn_per_point_image_list 
    return locals() 

def download():  
    return response.download(request, db) 

def get_my_file():
    if len(request.args)==2:
        filename=request.args[0]+request.args[1]+'.png'
    else:
        filename=request.args[0]
    print filename
    path=os.path.join(request.folder,'uploads',filename)
    #response.headers['Content-Type']='image/png'
    response.headers['ContentType'] ="application/octet-stream";
    response.headers['Content-Disposition']="attachment; filename="+filename
    return response.stream(open(path),chunk_size=4096)
