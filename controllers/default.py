from PIL import Image
import os
import traceback
import gluon.contrib.simplejson as json

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
    return locals()

def remove_the_register():
    try:
        print "in remove_the_register"
        img_id = request.args[0]
        db(db.t_point_pattern.doc_id==img_id).delete()
    except:
        return "alert(JSON.stringify('%s'));"  % json.dumps(traceback.format_exc())
    return "window.location.reload();"
    #return "alert('xx');jQuery('#caculate_div_%s').load('%s');" % (img_id,URL('feature_caculate_div',args=[1]))

def image_register():
    try:
        print "in image_register"
        img_id = request.args[0]
        import image_register as img_register
        img_register.hash_table =MyHashTable(db) 
        record = db.t_point_pattern(doc_id=img_id)
        if record is None:
            img_record = db.t_doc_image(id=img_id)
            f = img_record.internal_filename
            f = os.path.join(request.folder,'uploads',f)
            img = Image.open(f)
            img_register.image_register(img,img_id)
    except:
        db.rollback()
        return "alert(JSON.stringify('%s'));"  % json.dumps(traceback.format_exc())
        
    return "window.location.reload();"
    #return "jQuery('#caculate_div_2').html('<h2>abc</h2>');"
    #return "jQuery('#caculate_div_%s').load('%s');" % (img_id,URL('feature_caculate_div',args=[1]))

def ndex():
    link_list=[]
    base_url='http://'+request.env.http_host+'/'+request.application+'/'
    links = ["hello/action2","hello/action1"]
    links += ["form2/display_your_form"]
    links += ["form1/first","form1/second"]
    links += ["show_env/request","show_env/all"]
    links += ["form_crud/all_records","form_crud/update_your_form"]
    links += ["form_validation/display_your_form"]
    links += ["show_file/show_txt_file/test.txt"]
    links += ["show_file/show_image_file/test.png"]
    links += ["image_blog/index"]
    links += ["image_blog/upload_and_show_all"]
    links += ["upload_resize_image/upload_show"]
    links += ["upload_resize_image/upload_resize"]
    links += ["do_matplot"]
    for i in links:
        link_list.append((i, base_url+i))
    return dict(link_list=link_list)


def download():  
    return response.download(request, db) 
