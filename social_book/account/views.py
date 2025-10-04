from django.shortcuts import render, redirect,HttpResponse
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .db_engine import *
from .db_engine import engine,engine1
import pandas as pd
from sqlalchemy import text
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.viewsets import ModelViewSet
from .serializers import UserFileSerializer
from .decorators import check_uploaded_files
import random
from django.core.mail import send_mail
from django.conf import settings


# Create your views here.
#email notification on login to specific user
def user_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)
        if user:
            otp = str(random.randint(1000, 9999))
            request.session["otp"] = otp
            request.session["user_id"] = user.id

            send_mail(
                subject="Your Login OTP",
                message=f"Hello {user.username},\nYour OTP is {otp}.",
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[user.email],
            )
            return redirect("verify_otp")

        return HttpResponse("Invalid credentials")
    return render(request, "accounts/login.html")


def verify_otp(request):
    if not request.user.is_authenticated:
        return redirect('login')
    if request.method == "POST":
        otp_entered = request.POST.get("otp")
        otp_session = request.session.get("otp")
        user_id = request.session.get("user_id")

        if otp_entered == otp_session:
            user = CustomUser.objects.get(id=user_id)
            login(request, user)

            request.session.pop("otp", None)
            request.session.pop("user_id", None)

            return redirect("authors_sellers")
        else:
            return HttpResponse("Invalid OTP ❌")
    data=CustomUser.objects.get(id=request.session.get("user_id"))
    return render(request, "accounts/verify_otp.html",{"email": data.email})

def register(request):
    if request.method=='POST':
        username=request.POST['username']
        email=request.POST['email']
        public_visibility=request.POST.get('public_visibility') == 'True'
        password=request.POST['password']
        password1=request.POST['password1']
        if password != password1:
            return HttpResponse("Password Mismatch")    
        CustomUser.objects.create_user(username=username, password=password, email=email, public_visibility=public_visibility)
        return redirect('login')
    return render(request,'accounts/register.html')

def dashboard(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    return render(request,'accounts/index.html',{ 'user':request.user })

def user_logout(request):
    logout(request)
    return redirect('login')    

def authors_and_sellers(request):
    if not request.user.is_authenticated:
        return redirect('login')
    users = CustomUser.objects.filter(public_visibility=True) & (CustomUser.objects.exclude(id=request.user.id))
    return render(request, "accounts/authors_sellers.html", {"users": users})
    
#file upload mechanism
def upload_book(request):
    if not request.user.is_authenticated:
        return redirect('login') 
    if not request.user.is_authenticated:
        return redirect('login')
    
    if request.method == "POST":
        title = request.POST['title']
        description = request.POST['description']
        file = request.FILES['file']
        visibility = 'visibility' in request.POST
        cost = request.POST['cost']
        year_of_publication = request.POST['year_of_publication']
        
        UploadedFile.objects.create(
            user=request.user,
            title=title,
            description=description,
            file=file,
            visibility=visibility,
            cost=cost,
            year_of_publication=year_of_publication
        )
        return redirect('authors_sellers')
    
    return render(request, "accounts/Upload_Books.html")

#dashboard to view all registered user
    
def show_books(request, user_id):
    if not request.user.is_authenticated:
        return redirect('login')    
    user = CustomUser.objects.get(id=user_id)
    books = UploadedFile.objects.filter(user=user, visibility=True)
    return render(request, "accounts/user_books.html", {"books": books, "user": user})

# postgresql Database Connection 
    
def connect_db(request):
    with engine.connect() as conn:
        result = conn.execute(text("SELECT * FROM emp"))
        employees = [dict(row._mapping) for row in result]
        for i in employees:
            print(i)    
    html = "<h1>Database connected successfully.</h1>"
    html += "<br><h2>Employees Data:</h2><ul>"
    for emp in employees:
        html += f"<li>{emp}</li>"
    html += "</ul>"
    return HttpResponse(html)

# try to connect MySQL Database 
    
def connect_mysql_db(request):
    df= pd.read_sql_table("student", engine1,columns=["name"])
    print(df)
    try:
        with engine1.connect() as conn:
            result = conn.execute(text("SELECT * FROM student"))  
            data = [dict(row._mapping) for row in result]
        html = "<h1>MySQL Database connected successfully.</h1>"
        html += "<br><h2>Data:</h2><ul>"
        for item in data:
            html += f"<li>{item}</li>"
        html += "</ul>"

        return HttpResponse(html)

    except Exception as e:
        return HttpResponse(f"Error: {str(e)}")
#create api to login and fetch uploaded files , here i use postman to genrate token and fetch only his uploaded files
class UserFilesView(ModelViewSet):
    permission_classes = [AllowAny]  # only logged-in users
    serializer_class = UserFileSerializer
    def get_queryset(self):
        return UserFile.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
#use of wrappers and redirect urls
@check_uploaded_files
def user_files_dashboard(request):
    if not request.user.is_authenticated:
        return redirect('login')    
    files = UploadedFile.objects.filter(user=request.user)
    return render(request, 'accounts/user_books.html', {'files': files})

