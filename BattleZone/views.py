from django.shortcuts import redirect, render
from django.contrib.auth import logout, authenticate, login
from django.contrib import messages
from BattleZone.models import PersonalInfo2, Room, Player
from django.contrib.auth.models import User
import random
from datetime import datetime
from BattleZone.player_add_remove import addPlayer, removePlayer

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
            return redirect('/welcomeNote')

        else:
            messages.error(request, 'Oops! Seems you entered wrong credentials')

    if request.user.is_anonymous:
        context = {'loginStatus' : False}
        return render(request, 'register.html', context)
    else:
        context = {'loginStatus' : True}
        return render(request, 'welcomeNote.html', context)

def signUp(request):
    if request.method=="POST":
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        city = request.POST.get('city')
        gender = request.POST.get('GenderOptions')
        occupation = request.POST.get('OccupationOptions')
        language = request.POST.get('language')

        if User.objects.filter(email=email).exists():
            messages.warning(request, 'This user already exists')
            return redirect('/signUp')

        if User.objects.filter(username=username).exists():
            messages.warning(request, 'This username isn\'t available')
            return redirect('/signUp')
        
        user = User.objects.create_user(username, email, password)
        user.first_name = first_name
        user.last_name = last_name
        add_info = PersonalInfo2()
        add_info.City = city
        add_info.Gender = gender
        add_info.Occupation = occupation
        add_info.PreferredProgrammingLanguage = language
        user.personalinfo2 = add_info
        add_info.save()
        user.save()
        messages.success(request, 'Wohoo!! Your Account has been created successfully!')
        return redirect('/sign_in')

    if request.user.is_anonymous:
        return render(request, 'signup.html')
    else:
        return redirect('/welcomeNote')
    

def welcomeNote(request):
    if request.user.is_anonymous:
        return redirect('/sign_in')
    else:
        context = {'loginStatus' : True}
        return render(request, 'welcomeNote.html', context)

def room(request):
    loginStatus = True
    if request.user.is_anonymous:
        return redirect('/sign_in')
    context = {
        'loginStatus' : loginStatus,
    }
    return render(request, 'room.html', context)

def createRoom(request):
    loginStatus = True
    if request.user.is_anonymous:
        return redirect('/sign_in')
    context = {
        'loginStatus' : loginStatus,
    }

    if request.method=="POST":
        if Room.objects.filter(room_admin=request.user.username):
            room = Room.objects.get(room_admin=request.user.username)
            room.delete()

    return render(request, 'createRoom.html', context)

def enterRoom(request):
    loginStatus = True
    if request.method == "POST":
        room_code = request.POST.get('room_code')
        room = Room.objects.get(room_code=room_code)
        player1 = request.user
        removePlayer(room=room, player=player1)

    if request.user.is_anonymous:
        return redirect('/sign_in')
    context = {
        'loginStatus' : loginStatus,
    }
    return render(request, 'enterRoom.html', context)

def playersPage(request):
    loginStatus = True
    if request.user.is_anonymous:
        return redirect('/sign_in')

    if request.method=="POST":
        currentPlayersCount = 0
        admin_user = None
        if 'create_room' in request.POST:
            admin_user = True
            no_of_questions = int(request.POST.get('no_of_questions'))

            if Room.objects.filter(room_admin=request.user.username).exists():
                room = Room.objects.get(room_admin=request.user.username)
                currentPlayersCount = room.currentPlayersCount
                messages.info(request, 'You can\'t create or join another room until you delete this room')
                return redirect('/playersPage')

            else:
                room_code = random.randint(100000,999999)
                while Room.objects.filter(room_code=room_code).exists():
                    room_code = random.randint(100000,999999)
                
                player1 = request.user
                player_node = Player(prev=None, player=player1, next=None)
                player_node.save()
                room = Room(room_code=room_code, room_admin=request.user.username, no_of_questions=no_of_questions, currentPlayersCount=1, date=datetime.today(), head=player_node, tail=player_node)
                room.save()
                player_node.in_room = room
                player_node.save()
                currentPlayersCount = room.currentPlayersCount

        elif 'enter_room' in request.POST:
            user = request.user
            if Player.objects.filter(player=user).exists():
                player = Player.objects.get(player=user)
                room = player.in_room
                messages.warning(request,f'You\'re already in the room {room.room_code}. Please leave this room first.')
                return redirect('/playersPage')

            admin_user = False
            room_code = request.POST.get('room_code')
            if Room.objects.filter(room_code=room_code).exists():
                room = Room.objects.get(room_code=room_code)
                if room.currentPlayersCount >=4:
                    messages.warning(request, 'Sorry! This room is full.')
                    return redirect('/room')
                player1 = request.user
                addPlayer(player=player1, room=room)
                
            else:
                messages.info(request, 'This room doesn\'t exist')
                return redirect('/enterRoom')
            currentPlayersCount = room.currentPlayersCount

    else:
        user = request.user
        if Player.objects.filter(player=user).exists():
            player = Player.objects.get(player=user)
            room = player.in_room
            currentPlayersCount = room.currentPlayersCount
            if request.user.username == room.room_admin:
                admin_user = True
            else:
                admin_user = False
        else:
            messages.warning(request, 'Please Create or join a room first.')
            return redirect('/room')


    context= {
        'roomCode': room.room_code,
        'players' : range(1,currentPlayersCount+1),
        'loginStatus': loginStatus,
        'roomAdmin': room.room_admin,
        'admin_user': admin_user,
    }
    return render(request, 'players.html', context)

def logoutUser(request):
    logout(request)
    return redirect('/')

def about(request):
    loginStatus = True
    if request.user.is_anonymous:
        loginStatus = False
    context = {
        'loginStatus' : loginStatus,
    }
    return render(request, 'about.html', context)
    
def ide(request):
    if Room.objects.filter(room_admin=request.user.username):
        room = Room.objects.get(room_admin=request.user.username)
        no_of_questions = int(room.no_of_questions)
        loginStatus = True
        if request.user.is_anonymous:
            return redirect('/sign_in')
        context = {
            'loginStatus' : loginStatus,
            'no_of_questions': range(1,no_of_questions+1),
        }
        return render(request, 'ide.html', context)
    else:
        return redirect('/createRoom')
