
from base64 import urlsafe_b64encode
import email
from email import message
import imp
from django.conf import settings
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as django_logout
from loginprjct import settings
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from . tokens import generate_token
from django.core.mail import EmailMessage,send_mail
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode

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

        if User.objects.filter(username=username):
            messages.error(request,"Username already exist. Please choose another username")
            return redirect('home')
        if User.objects.filter(email=email):
            messages.error(request,"Email already registered")
            return redirect('home')

        if len(username)>10:
            messages.error(request, "Username must be under 10 characters")

        if pass1 != pass2:
            messages.error(request, "Passwords didn't match")
        
        if not username.isalnum():
            messages.error(request, "Username must be alpha- numeric")
            return redirect('home')

        myuser = User.objects.create_user(username, email, pass1)
        myuser.firstname = fname
        myuser.lastname = lname
        myuser.is_active = False
        myuser.save()

        messages.success(request, "Your account has been successsfully created. We have send you a conformation email, Please confirm your email in order to activate your account ")
    
        #welcome email
        subject = "welcome to loginsym!"
        message = " Hello " + myuser.firstname + "!! \n" + "welcome to loginsym!! \n Thank you \n we have also sent you a conformation email, please conform your email address in order to activate your account \n \n Thank you"
        from_email = settings.EMAIL_HOST_USER
        to_list = [myuser.email]
        send_mail(subject,message,from_email,to_list,fail_silently=True)

        #Email address conformation email

        current_site = get_current_site(request)
        email_subject = 'Confirm your email @ loginsym loginprjct login!!'
        message2 = render_to_string('email_confirmation.html',{
            'name': myuser.firstname,
            'domain': current_site.domain,
            'uid' : urlsafe_b64encode(force_bytes(myuser.pk)),
            'token' : generate_token.make_token(myuser)
        })
        email = message.EmailMessage(
            email_subject,
            message2,
            settings.EMAIL_HOST_USER,
            [myuser.email],
        )
        email.fail_silently = True
        email.send()

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
    django_logout(request)
    messages.success(request, "Logged out successfully!")
    return redirect('home')

def activate(request,uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        myuser = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        myuser = None

    if myuser  is not None and generate_token.check_token(myuser, token):
        myuser.is_active = True
        myuser.save()
        auth_login(request, myuser)
        return redirect('home')
    else:
        return render(request, 'activation_failed.html')
