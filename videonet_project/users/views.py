from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("video_list")
    else:
        form = UserCreationForm()
    return render(request, "users/register.html", {"form": form})

def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("video_list")
    else:
        form = AuthenticationForm()
    return render(request, "users/login.html", {"form": form})

@login_required
def delete_account(request):
    if request.method == "POST":
        request.user.delete()
        return redirect("video_list")
    return render(request, "users/delete_account.html")

@login_required
def logout_view(request):
    logout(request)
    return redirect("login")