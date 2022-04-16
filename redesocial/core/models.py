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
    
class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    post_text = models.CharField(max_length=2000)
    post_picture = models.FileField(default='default.jpg',
                                    upload_to='post_picture')
    
    def __str__(self) -> str:
        return self.user.username
    
#armazena pessoas que seguiu   
class Following(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    following_user = models.CharField(max_length=100, null=True)
    
    def __str__(self) -> str:
        return self.following_user.username
    
class Follower(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    follower_user = models.CharField(max_length=100, null=True)
    
    def __str__(self) -> str:
        return self.follower_user.username
    
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_text = models.CharField(default="", max_length=2000)