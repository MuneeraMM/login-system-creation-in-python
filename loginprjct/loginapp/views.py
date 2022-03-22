
import email
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
# Create your views here.
def home(request):
    return render(request,"index.html")

def sigup(request):
    if request.method == "POST":
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        myuser = User.objects.create_user(username, email, pass1)
        myuser.firstname = fname
        myuser.lastname = lname

        myuser.save()

        messages.success(request, "Your account has been successsfully created.")
    
        return redirect('signin')
    return render(request,"sigup.html")

def signin(request):

    if request.method == 'POST':
        username = request.POST ['username']
        pass1 = request.POST['pass1']
        user = authenticate(request, username=username, password=pass1)

        if user is not None:
            auth_login(request, user)
            fname = user.username
            return render(request,"index.html", {"fname":fname})
        else:
            messages.error(request, "Bad credentials")
            return redirect('home')

    return render(request,"signin.html")

def signout(request):
    pass
