from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import date
# Create your models here.
class CustomUser(AbstractUser):
    birth_year = models.IntegerField(null=True, blank=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    public_visibility = models.BooleanField(default=True)

    @property
    def age(self):
        if self.birth_year:
            return date.today().year - self.birth_year
        return None

class UploadedFile(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    file = models.FileField(upload_to="uploads/books/")
    visibility = models.BooleanField(default=True)
    cost = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    year_of_publication = models.PositiveIntegerField()

    def __str__(self):
        return self.title
class UserFile(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    file = models.FileField(upload_to="uploads/")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.file.name