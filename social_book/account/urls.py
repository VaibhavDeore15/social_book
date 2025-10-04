from django.urls import path, include
from django.contrib import admin
from .views import *
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter

router=DefaultRouter()
router.register(r'userfiles', UserFilesView, basename='userfiles')

urlpatterns = [
    path('', user_login, name='login'),
    path('register/', register, name='register'),
    path('dashboard/', dashboard, name='dashboard'),
    path('logout/', user_logout, name='logout'),
    path('authors-sellers/', authors_and_sellers, name='authors_sellers'),
    path('upload-book/', upload_book, name='upload_book'),
    path('my-books/', user_files_dashboard, name='my_book'),
    path('connect_db/', connect_db, name='connect_db'),
    path('verify_otp/', verify_otp, name='verify_otp'),
    path('connect_mysql_db/', connect_mysql_db, name='connect_mysql_db'),
    path('api/', include(router.urls)),
    
    
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)