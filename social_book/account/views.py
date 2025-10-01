from django.shortcuts import render, redirect,HttpResponse
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
# Create your views here.

def user_login(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request,user)
            return redirect('dashboard')
    return render(request,'accounts/login.html')

def register(request):
    if request.method=='POST':
        username=request.POST['username']
        email=request.POST['email']
        password=request.POST['password']
        password1=request.POST['password1']
        if password != password1:
            return HttpResponse("Password Mismatch")    
        User.objects.create_user(username=username, password=password, email=email)
        return redirect('login')
    return render(request,'accounts/register.html')

def dashboard(request):
    return HttpResponse("<h1>Welcome to Dashboard</h1>")