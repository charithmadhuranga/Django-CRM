from django.contrib.auth.models import User
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
    return redirect('login')

def signup_user(request):
    if request.user.is_authenticated:
        return redirect('crm')
    if request.method == 'POST':
        first_name = request.POST.get('firstName')
        last_name = request.POST.get('lastName')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        # Validate the form data
        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return redirect('signup')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken.")
            return redirect('signup')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered.")
            return redirect('signup')

        # Create the user
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password1,
            first_name=first_name,
            last_name=last_name
        )
        user.save()

        messages.success(request, "Signup successful! You can now log in.")
        return redirect('login')  # Replace 'login' with your login page URL name

    return render(request, 'signup.html')