from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
# Create your views here.


# @login_required(login_url='/login/')
# @login_required(login_url="/login/")
def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # if user doesn't exist
        if not User.objects.filter(username=username).exists():
            messages.error(request, 'Oops username not found')
            return redirect('/login/')
        user = authenticate(username=username, password=password)

        if user is None:
            messages.error(request, 'Invalid Password')
            return redirect('/login')
        else:
            login(request, user)
            return redirect('/')

    return render(request, 'login/login.html')

def logout_page(request):
    logout(request)
    return redirect('/login/')



def register_page(request):
    # data comming from above
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
    # check if user is already registered
        user = User.objects.filter(username=username)
        if user.exists():
            messages.error(request, 'Already a User')
            return redirect('/register')
        user = User.objects.create(username=username)

        # encrypt password
        user.set_password(password)
        user.save()
        messages.success(request, 'Account Created Succesfully')
        return redirect('/login/')
    return render(request, 'login/register.html')

@login_required(login_url="/login/")
def home(request):
    return render(request, 'home/home.html')
