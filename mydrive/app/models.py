from django.db import models

# Create your models here.
class Users(models.Model):
    name=models.TextField()
    email = models.EmailField(unique=True)
    password=models.TextField()
    
class filess(models.Model):
    user=models.ForeignKey(Users,on_delete=models.CASCADE)
    title=models.TextField()
    file=models.FileField(upload_to='upload/',null=True, blank=True)
