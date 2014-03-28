from PIL import Image
import os

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
    return dict(form=form, records=image_records)

def image_register():

    import image_register as img_register
    img_register.hash_table =MyHashTable(db) 
    img_id = request.args[0]
    rows = db(db.t_doc_image.id==img_id).select()
    f = rows.first().internal_filename
    f = os.path.join(request.folder,'uploads',f)
    img = Image.open(f)
    img_register.image_register(img,img_id)
    return DIV("%s" % str(img) + request.args[0])

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
