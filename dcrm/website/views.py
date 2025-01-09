from django.contrib.messages.context_processors import messages
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

# Create your views here.
def home(request):
    return render(request,'index.html',{})


def crm(request):
    if not request.user.is_authenticated:
        return redirect('login')
    return render(request,'crm.html',{})

def login_user(request):

    if request.user.is_authenticated:
        return redirect('crm')

    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            messages.success(request, 'You have successfully logged in')
            return redirect('crm')
        else:
            messages.success(request,'Username or Password is incorrect')
            return redirect('login')
    else:
        return render(request,'login.html',{})

def logout_user(request):
    logout(request)
    messages.success(request,'You have successfully logged out')
    return redirect('home')