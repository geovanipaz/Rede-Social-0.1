from pyexpat import model
from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_photo = models.FileField(default='default.jpg', 
                                     upload_to='profile_photos')
    status_info = models.CharField(default='Enter Status', max_length=1000)
    
    def __str__(self) -> str:
        return f'{self.user.username} Profile'
    

