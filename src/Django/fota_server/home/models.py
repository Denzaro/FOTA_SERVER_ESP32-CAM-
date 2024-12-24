from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class UserID(models.Model):
    user_id = models.CharField(max_length=255,default='')

class HexFile(models.Model):
    user_id = models.ForeignKey(UserID, on_delete=models.CASCADE)
    file_name = models.CharField(max_length=255, default="")  # File name for reference
    file_data = models.BinaryField()  # Binary data for file content
    uploaded_at = models.DateTimeField(auto_now_add=True)