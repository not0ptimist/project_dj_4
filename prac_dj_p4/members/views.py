from django.shortcuts import render, redirect
# https://docs.djangoproject.com/en/4.0/topics/auth/
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from .forms import RegisterUserForm

# Create your views here.
def login_user(request):
    # https://docs.djangoproject.com/en/4.0/topics/auth/default/#how-to-log-a-user-in
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
            # Redirect to a success page.
        else:
            # Return an 'invalid login' error message.
            messages.success(request, ('There was an Error logining, try again'))
            return redirect('login')
    else:
        return render(request, 'authenticate/login.html', {})

def logout_user(request):
    logout(request)
    messages.success(request, ('You were logout'))
    return redirect('home')

def register_user(request):
    if request.method == 'POST':
        form = RegisterUserForm(request.POST)# UserCreationForm сначало использовали
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']# потомучто будет еще проверка первого пароля со вторым
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, "Registration Sucesfull")
            return redirect('home')
    else:
        form = RegisterUserForm()
    return render(request, 'authenticate/register_user.html', {
        'form': form,
        })