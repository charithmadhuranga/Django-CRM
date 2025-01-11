from django.contrib.auth.models import User
from django.contrib.messages.context_processors import messages
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Record

# Create your views here.
def home(request):
    return render(request,'index.html',{})


def crm(request):
    if not request.user.is_authenticated:
        return redirect('login')
    records = Record.objects.all()
    return render(request,'crm.html',{ 'records':records })

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


def customer_record(request,pk):
    if not request.user.is_authenticated:
        return redirect('login')
    customer_record = Record.objects.get(id=pk)
    return render(request,'record.html',{'customer_record':customer_record})

def delete_record(request,pk):
    if not request.user.is_authenticated:
        return redirect('login')
    record = Record.objects.get(id=pk)
    record.delete()
    messages.success(request,'Record Deleted Successfully')
    return redirect('crm')

def add_record(request):
    if not request.user.is_authenticated:
        return redirect('login')
    if request.method == 'POST':
        first_name = request.POST.get('firstName')
        last_name = request.POST.get('lastName')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        city = request.POST.get('city')
        state = request.POST.get('state')
        zipcode = request.POST.get('zipcode')

        recordme = Record.objects.create(first_name=first_name, last_name=last_name, email=email, phone=phone, address=address, city=city, state=state, zipcode=zipcode)
        recordme.save()
        messages.success(request,'Record Added Successfully')

    return render(request,'add_record.html')

def update_record(request,pk):
    if not request.user.is_authenticated:
        return redirect('login')
    customer_record = Record.objects.get(id=pk)
    if request.method == 'POST':
        customer_record.first_name = request.POST.get('firstName')
        customer_record.last_name = request.POST.get('lastName')
        customer_record.email = request.POST.get('email')
        customer_record.phone = request.POST.get('phone')
        customer_record.address = request.POST.get('address')
        customer_record.city = request.POST.get('city')
        customer_record.state = request.POST.get('state')
        customer_record.zipcode = request.POST.get('zipcode')
        customer_record.save()
        messages.success(request,'Record Updated Successfully')
        return redirect('crm')
    return render(request,'update_record.html',{'customer_record': customer_record})