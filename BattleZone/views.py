from django.shortcuts import redirect, render
from django.contrib.auth import logout, authenticate, login
from django.contrib import messages

# Create your views here.
def index(request): 
    loginStatus = True
    if request.user.is_anonymous:
        loginStatus = False
    context = {
        'loginStatus' : loginStatus,
    }
    return render(request, 'index.html', context)

def sign_in(request): 
    loginStatus = False
    if request.method=="POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            loginStatus = True
            context = {'loginStatus' : loginStatus}
            return render(request, 'welcomeNote.html', context)

        else:
            messages.error(request, 'Oops! Seems you entered wrong credentials')

    if request.user.is_anonymous:
        context = {'loginStatus' : False}
        return render(request, 'register.html', context)
    else:
        context = {'loginStatus' : True}
        return render(request, 'welcomeNote.html', context)

def welcomeNote(request):
    if request.user.is_anonymous:
        return redirect('/sign_in')
    else:
        context = {'loginStatus' : True}
        return render(request, 'welcomeNote.html', context)

def room(request):
    loginStatus = True
    if request.user.is_anonymous:
        loginStatus = False
    context = {
        'loginStatus' : loginStatus,
    }
    return render(request, 'room.html', context)

def createRoom(request):
    loginStatus = True
    if request.user.is_anonymous:
        loginStatus = False
    context = {
        'loginStatus' : loginStatus,
    }
    return render(request, 'createRoom.html', context)

def enterRoom(request):
    loginStatus = True
    if request.user.is_anonymous:
        loginStatus = False
    context = {
        'loginStatus' : loginStatus,
    }
    return render(request, 'enterRoom.html', context)

def playersPage(request):
    context= {
        'players' : ['Sandeep','Vipul','Rajjo']
    }
    return render(request, 'players.html', context)

def signUp(request):
    loginStatus = True
    if request.user.is_anonymous:
        loginStatus = False
    context = {
        'loginStatus' : loginStatus,
    }
    return render(request, 'signup.html', context)

def logoutUser(request):
    logout(request)
    return redirect('/')