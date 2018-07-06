import string
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string
from django.db import models, connection, transaction
from django.http import HttpResponse
from vero import VeroEventLogger

from celery import shared_task
from .models import Usersettings


@shared_task
def export_to_getvero(username,user_id):
    tname = username+"_contacts"
    #user_id = User.objects.get(username=the_username).pk
    data = Usersettings.objects.get(user_id=user_id)
    #getvero_username = data.getvero_username[:1].get()
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

@shared_task
def create_user_table(username):
    sql = "CREATE TABLE `"+username+"_contacts` ("\
            "`id` int(11) NOT NULL AUTO_INCREMENT,"\
            "`first_name` varchar(45) NOT NULL,"\
            "`second_name` varchar(45) NOT NULL,"\
            "`town` varchar(45) DEFAULT NULL,"\
            "`country` varchar(45) DEFAULT NULL,"\
            "`telephone` varchar(20) NOT NULL,"\
            "`email` varchar(45) NOT NULL,"\
            "`date_of_birth` date DEFAULT NULL,"\
            "`created_at` date NOT NULL,"\
            "PRIMARY KEY (`id`)"\
            ") ENGINE=InnoDB DEFAULT CHARSET=utf8;"
    cursor = connection.cursor()
    cursor.execute(sql) 
    return 'table create'
    




