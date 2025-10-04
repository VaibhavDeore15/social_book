from django.contrib import admin
from .models import CustomUser, UploadedFile, UserFile
@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'birth_year', 'address', 'public_visibility', 'age')

admin.site.register(UploadedFile)
admin.site.register(UserFile)
# Register your models here.
