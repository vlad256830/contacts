from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.db import models, connection, transaction
from django.http import JsonResponse
from django.core import serializers
import datetime
from .forms import *
from .models import Usersettings

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
        data = Usersettings.objects.get(user_id=user_id)
        #for item in data:[:1].get()
        print(data.Getvero_key)
        context = {
            'username': username,
            'data' : data,            
        }
        return render(request,"contacts/mysettings.html",context)