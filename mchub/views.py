import re

from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt

from mchub import projects as proj

def new(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            return render(request, 'new.html', {'username': request.user.username})
        else:
            return redirect('/')
    else:
        proj_name = request.POST['name']
        if not re.match('^\w+$', proj_name):
            return render(request, 'new.html', {'not_available': True})
        elif proj.exist(request.user.username, proj_name):
            return render(request, 'new.html', {'existed': True})
        else:
            proj.create_project(request.user.username, proj_name)
            return redirect('/')

def login(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            return redirect('/')
        else:
            return render(request, 'login.html')
    else:
        username, password = request.POST['username'], request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user:
            auth.login(request, user)
            return redirect(request.GET.get('next') or '/')
        else:
            return render(request, 'login.html', {'not_found': True})

def logout(request):
    auth.logout(request)
    return redirect('/')

def root(request):
    if request.user.is_authenticated:
        return render(request, 'index-logined.html', {
            'username': request.user.username,
            'projects': proj.get_proj(request.user.username)
        })
    else:
        return render(request, 'index.html')

def signup(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            return redirect('/')
        else:
            return render(request, 'signup.html')
    else:
        username = request.POST['username']
        password = [request.POST['password'], request.POST['verify']]
        for user in User.objects.all():
            if user.username == username:
                return render(request, 'signup.html', {'existed': True})
        if not re.match('^\w+$', username):
            return render(request, 'signup.html', {'not_available': True})
        if len(username) < 3:
            return render(request, 'signup.html', {'not_available': True})
        if password[0] != password[1]:
            return render(request, 'signup.html', {'not_same': True})
        if len(password[0]) < 8:
            return render(request, 'signup.html', {'too_weak': True})
        else:
            proj.create_user(username)
            User.objects.create_user(username=username, password=password[0])
            return redirect('/login/')
