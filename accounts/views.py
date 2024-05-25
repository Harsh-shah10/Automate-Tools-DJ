from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout 
from .forms import SignupForm, LoginForm
from django.contrib.auth.decorators import login_required


# Create your views here.
# Home page
def index(request):
    return render(request, 'accounts/index.html')

# signup page
def user_signup(request):
    if request.user.is_authenticated:
        return redirect('home')  
     
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = SignupForm()
    return render(request, 'accounts/signup.html', {'form': form})

# login page
def user_login(request):
    if request.user.is_authenticated:
        return redirect('home')  
     
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)    
                return redirect('home')
    else:
        form = LoginForm()
    return render(request, 'accounts/login.html', {'form': form})

# logout page
@login_required
def user_logout(request):
    logout(request)
    return redirect('login')