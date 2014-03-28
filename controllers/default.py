
def index():
    return HTML(BODY(H2("abc"), 
                    H2(A('入库',_href=URL('upload'))),
                    H2(A('检索',_href=URL('retrieval')))
                    ))
def upload():
    form = SQLFORM(db.t_doc_image)
    uploaded_image_record=[]
    if form.accepts(request,session):
        response.flash = 'Thanks! The form has been submitted.'
        #accepted values
        uploaded_image_record = db(db.t_doc_image.id==form.vars.id).select()
        print uploaded_image_record
    elif form.errors:
        response.flash = 'Please correct the error(s).'
        #records = db().select(db.image.ALL)
    return dict(form=form, records=uploaded_image_record)


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
