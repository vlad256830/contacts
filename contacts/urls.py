from django.conf.urls import url


from .views import *

urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^register/$', register, name='register'),
    url(r'^contacts/$', contacts, name='contacts'),
    url(r'^login/$', login_user, name='login'),
    url(r'^logout/$', logout_user, name='logout'),
    url(r'^contacts/mycontacts/$', mycontacts, name='mycontacts'),
    url(r'^delete/$', contact_delete, name='delete'),
    #url(r'^basicupload/$', basicupload, name='basicupload'),
    url(r'^basicupload/$', importcsv, name='basicupload'),
    url(r'^contacts/addcontact/$', addcontact, name='addcontact'),
    #url(r'^contacts/importcsv/$', importcsv, name='importcsv'),
    url(r'^contacts/get-task-info/$', get_task_info, name='get-task-info'),
    url(r'^mysettings/$', mysettings, name='mysettings'),
    url(r'^mysettings/changepassword/$', changepassword, name='changepassword'),
    url(r'^mysettings/edit_getvero_key/$', edit_getvero_key, name='edit_getvero_key'),
    url(r'^exportcsv/$', exportcsv, name='exportcsv'),
    url(r'^exportvero/$', exportvero, name='exportvero'),
    url(r'^del_user_account/$', del_user_account, name='del_user_account'),
   

]