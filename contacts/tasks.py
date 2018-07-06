import string
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string
from django.db import models, connection, transaction
from django.http import HttpResponse
from vero import VeroEventLogger

from celery import shared_task
from .models import Usersettings


@shared_task
def my_task(username,user_id):
    tname = username+"_contacts"
    #user_id = User.objects.get(username=the_username).pk
    data = Usersettings.objects.filter(user_id=user_id)[:1].get()
    #getvero_username = data.getvero_username
    getvero_key = data.getvero_key
    #getvero connect
    logger = VeroEventLogger(getvero_key)
    
    cursor = connection.cursor()
    cursor.execute("SELECT `id`,`first_name`,`second_name`,`town`,`country`,`telephone`,`email`,"\
        "`date_of_birth`,`created_at` FROM `"+tname+"`")
    rows = cursor.fetchall()
    for s in rows:
        id =  s[0]
        user_email =s[6]
        user_data = {
            'first name': s[1],
            'last name': s[2],
            'town' : s[3],
            'country' : s[4],
            'telephone' : s[5],
            'date_of_birth': s[6],
        }
        logger.add_user(id, user_data, user_email=user_email)        
    return 'done'




