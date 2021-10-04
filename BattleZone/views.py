from django.shortcuts import render

# Create your views here.
def index(request): 
    return render(request, 'index.html')

def sign_in(request): 
    return render(request, 'register.html')

def welcomeNote(request):
    return render(request, 'welcomeNote.html')

def room(request):
    return render(request, 'room.html')

def createRoom(request):
    return render(request, 'createRoom.html')

def enterRoom(request):
    return render(request, 'enterRoom.html')

def playersPage(request):
    context= {
        'players' : ['Sandeep','Vipul','Rajjo']
    }
    return render(request, 'players.html', context)