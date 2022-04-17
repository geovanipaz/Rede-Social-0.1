from email import message
from pyexpat.errors import messages
from django.shortcuts import redirect, render
from .forms import CreateComment, UserForm, UpdateUserForm, UpdateProfileForm \
    ,CreatePost
from .models import User, Profile, Comment, Follower, Following
from django.contrib.auth.hashers import make_password
from django.contrib import messages



# Create your views here.
def index(request):
    return render(request,'core/index.html')

def verifyInput(username, password):
    error = []
    if len(username) < 4:
        error.append('Username deve ter mais de 4 caracters')
    elif len(password) < 8:
        error.append('Senha deve ter 8 caracteres ou mais')
    else:
        print('Ok')
    return error

def registerUser(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        hashed_password = make_password(password)
        
        error = verifyInput(username,password)
        
        if len(error) != 0:
            error = error[0]
            print(error)
            return render(request, 'core/registration_form.html', {'error':error})
        else:
            a = User(username=username, email=email, password=password)
            a.save()
            messages.success(request, 'Conta foi criada com sucesso')
            return redirect('register')
    else:
        return render(request, 'core/registration_form.html')