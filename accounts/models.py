from django.db import models

# Create your models here.

class Detail(models.Model):
    username = models.CharField(max_length=50)
    contact = models.CharField(max_length=10)
    profile = models.ImageField(upload_to='pics',null=True )
    hall = models.IntegerField(null=True)
    
