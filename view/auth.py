from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.models import User
from django.contrib import messages
from home.form import RegisterForm, LoginForm

# def register_view(request):
#     if request.method == 'POST':
#         form = RegisterForm(request.POST)
#         if form.is_valid():
#             user = form.save(commit=False)
#             user.email = form.cleaned_data['email']
#             user.save()

#             # Store extra fields in session
#             request.session['hospital_name'] = form.cleaned_data['hospital_name']
#             request.session['branch_name'] = form.cleaned_data['branch_name']
#             request.session['address'] = form.cleaned_data['address']
#             request.session['mobile_number'] = form.cleaned_data['mobile_number']

#             messages.success(request, "Registration successful!")
#             return redirect('login')
#     else:
#         form = RegisterForm()
#     return render(request, 'auth/register.html', {'form': form})

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Registration successful!")
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'auth/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                request,
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password']
            )
            if user is not None:
                login(request, user)
                return redirect('home')  # Replace with your dashboard/home view
            else:
                messages.error(request, "Invalid username or password")
    else:
        form = LoginForm()
    return render(request, 'auth/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login') 



