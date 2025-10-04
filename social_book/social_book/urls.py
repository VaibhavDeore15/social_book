
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('account.urls')),

    path('auth/', include('djoser.urls')),               # user registration, user management
    # path('auth/', include('djoser.urls.authtoken')), # token auth (DRF Token)
    path('auth/rest/', include('rest_framework.urls')),  
]

