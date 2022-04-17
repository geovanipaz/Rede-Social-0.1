from dataclasses import fields
from django.contrib.auth.models import User
from django import forms
from .models import Profile, Post, Comment

#form para registrar novo usuario
class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    email = forms.EmailField(max_length=254,help_text='Required Field')
    class Meta:
        model = User
        fields = ['username','email','password']
        
# form para atualizar email do usuario  
class UpdateUserForm(forms.ModelForm):
    email = forms.EmailField(max_length=254, help_text='Required Field')
    class Meta:
        model = User
        fields = ['email']

#form para atualizar perfil
class UpdateProfileForm(forms.ModelForm):
    class Meta:
        models = Profile
        fields = ['status_info', 'profile_photo']
        
#form para criar post
class CreatePost(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['post_text', 'post_picture']
        
#form para criar comentario
class CreateComment(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment_text']