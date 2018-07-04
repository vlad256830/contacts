from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model, authenticate, login, logout, update_session_auth_hash
from django.db import models, connection, transaction
from django.contrib.auth.forms import PasswordChangeForm
from django.http import JsonResponse
from django.core import serializers
from django.http import HttpResponse,HttpResponseForbidden
import datetime
import os
import csv
import io
from .models import Usersettings
from .forms import RegisterForm,ContactForm
from .tasks import my_task


User = get_user_model()


# Create your views here.
def index(request):
    context = {
        'form' : RegisterForm,
    }
    return render(request,"contacts/index.html",context)

def register(request):
    errors = []
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = RegisterForm(request.POST)        
        username = request.POST['username']
        email = request.POST['email']
        # check whether it's valid:
        if form.is_valid(): 
            email = form.clean_email()
            password = form.clean_password2()
            username = form.cleaned_data['username']         
            user = User.objects.create_user(username,email,password)
            user.save()  
             #create user table contacts
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
            context = {
                'result' : True,
            }
            return render(request, "contacts/register.html", context)
        else:            
            errors = form.errors
            context = {
                'result' : False,
                'errors' : errors,
                'form' : RegisterForm,
                'username' : username,
                'email' : email,
                
        }
        return render(request,"contacts/register.html",context)
        
    else:
        context = {
            'result' : False, 
            'form' : RegisterForm,
            'errors' : errors,
            'username' : '',
            'email' : '',
        }
        return render(request,"contacts/register.html",context)

def login_user(request):
    errors = []
    if request.method == 'POST':
        data = request.POST

        username = data['username']
        password = data['password']
        user = authenticate(request,username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("contacts:contacts")         
            
        else:
            errors.append('user password')
            context = {
                'errors' : errors,
                'username' : username,                
            }
            return render(request,"contacts/login.html",context)
    else:
        context = {
            'errors' : errors,
            'username' : '',
        }
        return render(request,"contacts/login.html",context)

def logout_user(request):
    logout(request)
    return render(request,"contacts/logout.html",{})


def mycontacts(request):
    username = None
    if request.user.is_authenticated():
        username = request.user.username
    if request.method == 'GET':
        tname = username+"_contacts"
        cursor = connection.cursor()
        cursor.execute("SELECT `id`,`first_name`,`second_name`,`town`,`country`,`telephone`,`email`,"\
        "`date_of_birth`,`created_at` FROM `"+tname+"`")
        rows = cursor.fetchall()

        columns = ['id','first_name','second_name','town','country','telephone','email','date_of_birth','created_at']
        obj = []
        #total_count = len(rows)
        for st in rows:
            ret= {}
            i = 0
            for col in columns:                
                ret[col] = st[i] 
                i += 1           
            obj.append(ret)

        context = {
            #"draw": 1,
            #"recordsTotal": 1,
            #"recordsFiltered": 1,
            "data": obj
            }
        #print(context)
        return JsonResponse(context)
        #return render(request, 'contacts/contacts.html', context)

def contacts(request):
   if request.user.is_authenticated():
        context = {}
        return render(request,"contacts/contacts.html",context)

def contact_delete(request):
     if request.method == 'POST':
        username = None
        id = request.POST['id']
        #print(id)
        if request.user.is_authenticated():
            username = request.user.username
            tname = username+"_contacts"
            sql = "DELETE FROM `"+tname+"` WHERE   `id`="+str(id)
            cursor = connection.cursor()
            cursor.execute(sql)
            context = {
                "error": [],
                "res": True,
            }
            return JsonResponse(context)


def addcontact(request): 
    username = None
    if request.user.is_authenticated():
        username = request.user.username
        if request.method == 'POST':
            form = ContactForm(request.POST)
            print(form)
            if form.is_valid(): 
                first_name = form.clean_first_name()
                second_name = form.clean_second_name()
                town = form.clean_town()
                country = form.clean_country()
                telephone = form.clean_telephone()                 
                dt = form.clean_date_of_birth()
                date_of_birth = '{:%Y-%m-%d}'.format(dt)
                email = form.clean_email()  
                created_at = '{:%Y-%m-%d}'.format(datetime.date.today())
                tname = username+"_contacts"
                sql = "INSERT INTO `" + tname + "`"\
                "(`first_name`,`second_name`,`town`,`country`,`telephone`,`email`,`date_of_birth`,`created_at`)VALUES"\
                "('"+first_name+"','"+second_name+"','"+town+"','"+country+"','"+telephone+"','"+email+"','"+date_of_birth+"','"+created_at+"')"
                cursor = connection.cursor()
                cursor.execute(sql) 
                context = {
                        "error": [],
                        "res": True,
                }
            
                return JsonResponse(context)
        #else:

def mysettings(request):
    username = None
    if request.user.is_authenticated():
        username = request.user.username
        user_id = request.user.id
        print(user_id)
        data = Usersettings.objects.filter(user_id=user_id)
        #for item in data:[:1].get()

        context = {
            'username': username,
            'data' : data,            
        }
        return render(request,"contacts/mysettings.html",context)

def changepassword(request):
    username = None
    error = []
    if request.user.is_authenticated():
        username = request.user.username
        if request.method == 'POST':
            form = PasswordChangeForm(user=request.user, data=request.POST)
            if form.is_valid():
                user = form.save()
                update_session_auth_hash(request, user)
            else:
                error.append('password invalid')
    else:
        error.append('user not authenticated')
    context = {
                "error": error,                
            }
    return JsonResponse(context)

def exportcsv(request, **kwargs):
    username = None
    if request.user.is_authenticated():
        username = request.user.username   
        tname = username+"_contacts"
        #task = generate_file.delay(tname)
        #return render(request,"contacts/exportvero.html",{"task_id": task.task_id })
        filename = tname+".csv"
        cursor = connection.cursor()
        cursor.execute("SELECT `id`,`first_name`,`second_name`,`town`,`country`,`telephone`,`email`,"\
        "`date_of_birth`,`created_at` FROM `"+tname+"`")
        rows = cursor.fetchall()
        columns = ['id','first_name','second_name','town','country','telephone','email','date_of_birth','created_at']

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename='+filename

        writer = csv.writer(response)
        writer.writerow(columns)
        for i in rows:
            writer.writerow([i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7], i[8],])
        return response

def exportvero(request):
    username = None
    if request.user.is_authenticated():
        username = request.user.username   
        tname = username+"_contacts"
        result = my_task.delay(10)
        print(result)
        return render(request, 'contacts/exportvero.html', context={'task_id': result.task_id})
