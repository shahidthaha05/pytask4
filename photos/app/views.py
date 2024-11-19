from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from .models import *
import os
from django.contrib.auth.models import User
from django.contrib import messages

# Create your views here.


def photo_login(req):
    if 'photo' in req.session:
        return redirect(admin_home)
    if 'user' in req.session:
        return redirect(user_home)
    if req.method=='POST':
        uname=req.POST['uname']
        password=req.POST['passwd']
        data=authenticate(username=uname,password=password)
        if data:
            if data.is_superuser:
                login(req,data)
                req.session['photo']=uname   #create session
                return redirect(admin_home)
            else:
                login(req,data)
                req.session['user']=uname   #create session
                return redirect(user_home)
        else:
            messages.warning(req,'Invalid username or password.')
            return redirect(photo_login)
    
    else:
        return render(req,'login.html')

def photo_logout(req):
    req.session.flush()          #delete session
    logout(req)
    return redirect(photo_login)

# ---------------admin--------------------
def admin_home(req):
    return render(req,'admin/home.html')


# ---------------user--------------------

def register(req):
    if req.method=='POST':
        name=req.POST['name']
        email=req.POST['email']
        password=req.POST['password']
        try:
            data=User.objects.create_user(first_name=name,email=email,password=password,username=email)
            data.save()
            return redirect(photo_login)
        except:
            messages.warning(req,'User already exists.')
            return redirect(register)
    else:
        return render(req,'user/register.html')

def user_home(req):
    if 'user' in req.session:
        data=Images.objects.all()
        return render(req,'user/home.html',{'data':data})
    else:
        return redirect(req,'photo_login')

def add_img(req):
    if 'user' in req.session:
        if req.method=='POST':
            img=req.FILES['img']
            user=User.objects.get(username=req.session['user'])
            data=Images.objects.create(img=img,user=user)
            data.save()
            return redirect(add_img)
        else:
            return render(req,'user/add_img.html')
    else:
        return redirect(photo_login)
    
def delete(req,pid):
    data=Images.objects.get(pk=pid)
    url=data.img.url
    og_path=url.split('/')[-1]
    os.remove('media/'+og_path)
    data.delete()
    return redirect('home.html')
