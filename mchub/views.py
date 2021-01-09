import re

from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt

from mchub import projects as proj

def issues(request, name, project):
    if not proj.has_proj(name, project):
        return redirect('/')
    else:
        if request.user.is_authenticated:
            return render(request, 'issues.html', {
                'detail': proj.get_configure(name, project),
                'logined': True,
                'name': name,
                'project': project,
                'tab': 'issues',
                'username': request.user.username
            })
        else:
            return render(request, 'issues.html', {
                'detail': proj.get_configure(name, project),
                'logined': False,
                'name': name,
                'project': project,
                'tab': 'issues',
                'username': ''
            })

def new(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            return render(request, 'new.html', {
                'logined': True,
                'username': request.user.username,
            })
        else:
            return redirect('/')
    else:
        proj_name = request.POST['name']
        description = request.POST['desp']
        if not re.match('^\w[\w-]*$', proj_name):
            return render(request, 'new.html', {'not_available': True})
        elif proj.exist(request.user.username, proj_name):
            return render(request, 'new.html', {'existed': True})
        else:
            proj.create_project(request.user.username, proj_name, description)
            return redirect('/')

def new_issue(request, name, project):
    if request.method == 'GET':
        if not proj.has_proj(name, project):
            return redirect('/')
        else:
            if request.user.is_authenticated:
                return render(request, 'new-issue.html', {
                    'detail': proj.get_configure(name, project),
                    'logined': True,
                    'name': name,
                    'project': project,
                    'tab': 'issues',
                    'username': request.user.username
                })
            else:
                return render(request, 'new-issue.html', {
                    'detail': proj.get_configure(name, project),
                    'logined': False,
                    'name': name,
                    'project': project,
                    'tab': 'issues',
                    'username': ''
                })
    else:
        title = request.POST['title']
        comment = request.POST['comment'] or None
        label = request.POST.get('label')
        if label == 'none':
            label = None
        print('title:', title)
        print('comment:', comment)
        print('label:', label)
        return redirect('/project/%s/%s/' % (name, project))

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

def project(request, name, project):
    if request.method == 'GET':
        if not proj.has_proj(name, project):
            return redirect('/')
        else:
            if request.user.is_authenticated:
                return render(request, 'project.html', {
                    'detail': proj.get_configure(name, project),
                    'logined': True,
                    'name': name,
                    'project': project,
                    'tab': 'code',
                    'username': request.user.username
                })
            else:
                return render(request, 'project.html', {
                    'detail': proj.get_configure(name, project),
                    'logined': False,
                    'name': name,
                    'project': project,
                    'tab': 'code',
                    'username': ''
                })
    else:
        description = request.POST['desp']
        website = request.POST['website']
        proj.set_configure(name, project, description, website)
        return render(request, 'project.html', {
            'detail': proj.get_configure(name, project),
            'logined': True,
            'name': name,
            'project': project,
            'tab': 'code',
            'username': request.user.username
        })

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
        if not re.match('^\w[\w-]*$', username):
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
