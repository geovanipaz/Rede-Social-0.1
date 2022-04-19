
from email import message
from pyexpat.errors import messages
from django.shortcuts import redirect, render
from .forms import CreateComment, UserForm, UpdateUserForm, UpdateProfileForm \
    ,CreatePost
from django.contrib.auth import authenticate,login
from django.contrib import auth
from django.urls import reverse
from .models import Post, User, Profile, Comment, Follower, Following
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import itertools


# Create your views here.
#def index(request):
#    return render(request,'core/index.html')

def verifyInput(username, password):
    error = []
    if len(username) < 4:
        error.append('Username deve ter mais de 4 caracters')
    elif len(password) < 5:
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
            a = User(username=username, email=email, password=hashed_password)
            a.save()
            
            user = User.objects.get(username=username)
            user_id = User.objects.values_list('id', flat=True).filter(username=user)
            print('User id:', user_id)
            Profile.objects.create(user_id=user_id)
            messages.success(request, 'Conta foi criada com sucesso')
            return redirect('register')
    else:
        return render(request, 'core/registration_form.html')
    
def index(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        if user is not None and user.is_active:
            auth.login(request, user)
            return redirect('welcome')
        else:
            messages.info(request, 'Usuario ou Senha Inválidos')
            return redirect('index')
    else:
        return render(request, 'core/index.html')
    
def dashboard(request):
    return render(request, 'core/dashboard.html')

def feed(request):
    try:
        post_all = Post.objects.all().order_by('created_at')
        print(post_all)
    except Exception as e:
        print(e)
        
    comment_form = CreateComment()
    username = request.user.username
    
    context = {
        'post_all': post_all,
        'comment_form': comment_form,
        'username':username,
    }
    
    return render(request,'core/feed.html', context)

def followweb(request, username):
    if request.user.username != username:
        if request.method == 'POST':
            lider = User.objects.get(username=username)
            disc = User.objects.get(username=request.user.username)
            
            lider.follower_set.create(follower_user=disc)
            disc.following_set.create(following_user=lider)
            
            url = reverse('profile', kwargs = {'username':username})
            
            return redirect(url)
        
def unfollowweb(request, username):
    if request.method == 'POST':
        lider = User.objects.get(username=username)
        disc = User.objects.get(username=request.user.username)
        
        lider.follower_set.create(follower_user=disc).delete()
        disc.following_set.create(following_user=lider).delete()
        
        url = reverse('profile', kwargs = {'username':username})
        
        return redirect(url)

def postweb(request, username):
    if request.method == 'POST':
        post_form = CreatePost(request.POST, request.FILES)
        if post_form.is_valid():
            post_text = post_form.cleaned_data['post_text']
            post_picture = post_form.cleaned_data['post_picture']
            request.user.post_set.create(
                post_text=post_text,
                post_picture=post_picture)
            messages.success(request,f'Post criado com Sucesso')
    url = reverse('profile', kwargs={'username':username})
    return redirect(url)

def commentweb(request, username, post_id):
    if request.method == 'POST':
        comment_form = CreateComment(request.POST)
        if comment_form.is_valid():
            comment_text = comment_form.cleaned_data['comment_text']
            
            user = User.objects.get(username=username)
            post = user.post_set.get(pk=post_id)
            
            post.comment_set.create(user=request.user, comment_text=comment_text)
            messages.success(request,f'Comentário criado com Sucesso')
    url = reverse('profile', kwargs={'username':username})
    return redirect(url)

# view de busca
def search(request):
    template='core/search.html'

    query = request.GET['q']
    print(query)
    data = query

    count = {}
    results = {}
    results['posts']= User.objects.none()
    queries = data.split()
    for query in queries:
        results['posts'] = results['posts'] | User.objects.filter(username__icontains=query)
        count['posts'] = results['posts'].count()


    count2 = {}
    queries2 = data.split()
    results2 = {}
    results2['posts'] = User.objects.none()
    queries2 = data.split()
    for query2 in queries:
        results2['posts'] = results2['posts'] | User.objects.filter(first_name__icontains=query2)
        count2['posts'] = results2['posts'].count()


    count3 = {}
    queries3 = data.split()
    results3 = {}
    results3['posts'] = User.objects.none()
    queries3 = data.split()
    for query3 in queries:
        results3['posts'] = results3['posts'] | User.objects.filter(last_name__icontains=query3)
        count3['posts'] = results3['posts'].count()
        

    files = itertools.chain(results['posts'],results2['posts'], results3['posts'])
    result = []
    for i in files:
        if i not in result:
            result.append(i)    

    paginate_by=2
    username = request.user.username
    print('current user',username)
    person = User.objects.get(username = username)
    print('person',person)
	
    context={ 'files':result }
    return render(request,template,context)

def profile(request, username):
    if request.method == 'POST':
        u_form = UpdateUserForm(request.POST, instance=request.user)
        p_form = UpdateProfileForm(request.POST, request.FILES, instance=request.user.profile)
        
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            
            messages.success(request, f'Seu Perfil foi atualizado')
            url = reverse('profile', kwargs={'username':username})
            return redirect(url)
    else:
        if username == request.user.username:
            u_form = UpdateUserForm(instance=request.user)
            p_form = UpdateProfileForm(instance=request.user.profile)
            post_form = CreatePost()
            person = User.objects.get(username=username)
            
            context = {
                'u_form':u_form,
                'p_form':p_form,
                'post_form':post_form,
                'person': person
            }
        else:
            person = User.objects.get(username=username)
            already_a_follower = 0
            for followers in person.follower_set.all():
                if(followers.follower_user == request.user.username):
                    already_a_follower = 1
                    break
            if already_a_follower == 1:
                context = {
                    'person':person
                }
            else:
                context = {
                    'person':person,
                    'f':1,
                }
        comment_form = CreateComment()
        context.update({'comment_form':comment_form})
    return render(request, 'core/profile.html', context)

def welcome(request):
    url = reverse('profile', kwargs = {'username' : request.user.username})
    return redirect(url)
	