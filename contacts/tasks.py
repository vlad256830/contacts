import string
import os
import io
import datetime
import requests
from django.contrib.auth.models import User
#from django.utils.crypto import get_random_string
from django.db import models, connection, transaction
from django.http import HttpResponse
from celery import shared_task,current_task

from vero import VeroEventLogger

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

@shared_task   
def insert_csv_to_table(username,fname, count):
    tname = username+"_contacts"
    created_at = '{:%Y-%m-%d}'.format(datetime.date.today())
    try:
        with open(fname, "r", encoding="utf8") as f:
            content = f.readlines()        
            x = 0
            i = 0
            base_sql = "INSERT INTO `"+tname+"` (`first_name`,`second_name`,`town`,`country`,`telephone`,`email`,`date_of_birth`,`created_at`)VALUES"
            values_sql = ''
            sql = ''
            for line in content:         
                if not line.startswith("first"):
                    line = line.replace("\n","").replace("\r","")
                    print(line)
                    s = line.split(",")
                    if values_sql:
                        values_sql += ",('"+s[0]+"','"+s[1]+"','"+s[2]+"','"+s[3]+"','"+s[4]+"','"+s[5]+"','"+s[6]+"','"+created_at+"')"
                    else:
                        values_sql += "('"+s[0]+"','"+s[1]+"','"+s[2]+"','"+s[3]+"','"+s[4]+"','"+s[5]+"','"+s[6]+"','"+created_at+"')"
                    i += 1
                    x += 1
                    if x == 1000:                        
                        sql = base_sql+values_sql
                        cursor = connection.cursor()
                        cursor.execute(sql)
                        x = 0
                        values_sql = ''
                        current_task.update_state(state='PROGRESS', 
                                        meta={'current': i, 'total': count,
                                        'percent': int((float(i) / count) * 100)})


            sql = base_sql+values_sql
            cursor = connection.cursor()
            cursor.execute(sql)
            current_task.update_state(state='PROGRESS', 
                                        meta={'current': i, 'total': count,
                                        'percent': 100})
        
        os.remove(fname)
        return {'current': count, 'total': count, 'percent': 100}
    except: 
        return {'current': 0, 'total': count, 'percent': 0}

@shared_task 
def import_from_getvero(username,user_id):
    r = requests.get('https://api.github.com', auth=('username', 'pass'))

    print(r.status_code)
    print(r.headers['content-type'])
    
    return 'data import'



