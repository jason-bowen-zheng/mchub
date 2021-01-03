from django.contrib import auth
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt

def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    else:
        name, password = request.POST['username'], request.POST['password']
        print(name, password)
        return redirect('/')

@csrf_exempt
def logout(request):
    request.COOKIE.delete_cookie('is_login')
    request.COOKIE.delete_cookie('user')
    return redirect('/')

def root(request):
    return render(request, 'index.html')

def signup(request):
    return render(request, 'signup.html')
