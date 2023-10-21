from django.shortcuts import render, redirect
from .forms import RegisterForm
from django.contrib.auth.models import User
from .utils import check_email
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
# Create your views here.


def register(request):
    if request.method == 'GET':
        return render(request, 'register.html', {'form': RegisterForm()})
    else:
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 == password2:
            username_taken = User.objects.filter(username=username).exists()
            email_taken = User.objects.filter(email=email).exists()

            if username_taken:
                error = 'This username is taken. Try again!'
            if email_taken:
                error = 'This email is taken. Try again!'

            if not username_taken and not email_taken:
                email_valid = check_email(email)
                if email_valid:
                    try:
                        validate_password(password1)
                    except ValidationError as e:
                        return render(request, 'register.html', {'password_errors': e.messages, 'form': RegisterForm()})
                    else:
                        user = User.objects.create_user(
                            username=username, email=email, password=password1)
                        return redirect('home')
                else:
                    error = 'Invalid email. Try again!'

        else:
            error = 'Passwords did not match. Try again!'

        return render(request, 'register.html', {'form': RegisterForm(), 'error': error})


def login_user(request):
    if request.method == 'GET':
        return render(request, 'login_user.html', {'form': AuthenticationForm()})
    else:
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            user_exists = User.objects.filter(username=username).exists()
            if user_exists:
                error = 'Incorrect password.'
            else:
                error = f'User with username: {username} does not exist.'
            return render(request, 'login_user.html', {'form': AuthenticationForm(), 'error':error}) 

@login_required  
def logout_user(request):
    logout(request)
    return redirect('home')
