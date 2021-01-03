from django.contrib import auth
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt

def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    else:
        username, password = request.POST['username'], request.POST['password']
        user = auth.authenticate(username=username, password=password)
        return render(request, 'login.html', {'no_user_found': True})

@csrf_exempt
def logout(request):
    request.COOKIE.delete_cookie('is_login')
    request.COOKIE.delete_cookie('user')
    return redirect('/')

def root(request):
    return render(request, 'index.html')

def signup(request):
    if request.method == 'GET':
        return render(request, 'signup.html')
    else:
        username = request.POST['username']
        password = [request.POST['password'], request.POST['verify']]
        if password[0] != password[1]:
            return render(request, 'signup.html', {'not_same': True})
        if len(password[0]) < 8:
            return render(request, 'signup.html', {'too_weak': True})
        for user in User.objects.all():
            if user.username == username:
                return render(request, 'signup.html', {'not_available': True})
        else:
            User.objects.create(username=username, password=password[0])
            return redirect('/login/')
