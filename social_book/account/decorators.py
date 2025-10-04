# books/decorators.py
from django.shortcuts import redirect
from functools import wraps
from .models import UploadedFile,UserFile

def check_uploaded_files(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if UploadedFile.objects.filter(user=request.user).exists() :
            return view_func(request, *args, **kwargs)
        else:
            return redirect('upload_book')
    return wrapper

