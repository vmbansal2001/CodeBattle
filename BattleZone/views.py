from os import error
from typing import Text
from django.shortcuts import redirect, render
from django.contrib.auth import logout, authenticate, login
from django.contrib import messages
from BattleZone.models import PersonalInfo2, Room, Player
from django.contrib.auth.models import User
import random
from datetime import datetime
from BattleZone.player_add_remove import addPlayer, removePlayer
from BattleZone.codeExecution import executeUserPythonCode, executeUserJavaCode, executeUserCPPCode

# Home Page
def index(request): 
    loginStatus = True
    if request.user.is_anonymous:
        loginStatus = False
    context = {
        'loginStatus' : loginStatus,
    }
    return render(request, 'index.html', context)






# Practice
def practice(request):
    return render(request, 'practice.html')







# Sign-In Page
def sign_in(request): 
    if request.method=="POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('/welcomeNote')

        else:
            messages.error(request, 'Oops! Seems you entered wrong credentials')

    if request.user.is_anonymous:
        context = {'loginStatus' : False}
        return render(request, 'register.html', context)
    else:
        # If a user is already logged in, then redirect to Welcome Page
        context = {'loginStatus' : True}
        return render(request, 'welcomeNote.html', context)







#Sign - Up Page
def signUp(request):
    if request.method=="POST":
        #Get all info from request
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        city = request.POST.get('city')
        gender = request.POST.get('GenderOptions')
        occupation = request.POST.get('OccupationOptions')
        language = request.POST.get('language')

        #If user already exists, then redirect to Sign-In Page
        if User.objects.filter(email=email).exists():
            messages.warning(request, 'This user already exists')
            return redirect('/sign_in')

        #Username isn't available
        if User.objects.filter(username=username).exists():
            messages.warning(request, 'This username isn\'t available')
            return redirect('/signUp')
        
        #Create new User
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
        #If user already logged-in, then redirect to Welcome Page
        return redirect('/welcomeNote')
    






#Welcome Page for registered Users
def welcomeNote(request):
    #If user is not logged in, redirect to login page
    if request.user.is_anonymous:
        return redirect('/sign_in')
    else:
        context = {'loginStatus' : True}
        return render(request, 'welcomeNote.html', context)






#Room Page to ask to create for a new room, or enter an existing one
def room(request):
    if request.user.is_anonymous:
        return redirect('/sign_in')
    context = {'loginStatus' : True}
    return render(request, 'room.html', context)






#Create room page which asks the no. of questions from the user
def createRoom(request):
    if request.user.is_anonymous:
        return redirect('/sign_in')
    context = {'loginStatus' : True}

    #Request to delete the room
    if request.method=="POST":
        if Room.objects.filter(room_admin=request.user.username):
            room = Room.objects.get(room_admin=request.user.username)
            room.delete()
    return render(request, 'createRoom.html', context)








#Enter room page which asks for the room code from the user
def enterRoom(request):
    if request.user.is_anonymous:
        return redirect('/sign_in')

    #Request to leave a room
    if request.method == "POST":
        room_code = request.POST.get('room_code')
        room = Room.objects.get(room_code=room_code)
        player1 = request.user
        removePlayer(room=room, player=player1)

    context = {'loginStatus' : True}
    return render(request, 'enterRoom.html', context)







#Players Page which shows a proper room, and all players present in the room
def playersPage(request):
    loginStatus = True
    if request.user.is_anonymous:
        return redirect('/sign_in')

    #All requests handled here, further requests are routed
    if request.method=="POST":
        admin_user = None
        #Handles request to create a new room
        if 'create_room' in request.POST:
            user = request.user

            #If the user is already in a room, then redirect to old room
            if Player.objects.filter(player=user).exists():
                player = Player.objects.get(player=user)
                room = player.in_room
                messages.warning(request,f'You\'re already in the room {room.room_code}. Please leave this room first to join or create a new room.')
                return redirect('/playersPage')

            admin_user = True
            no_of_questions = int(request.POST.get('no_of_questions'))

            #If room admin is already associated with any other room, redirect to old room
            if Room.objects.filter(room_admin=request.user.username).exists():
                messages.info(request, 'You can\'t create or join another room until you delete this room')
                return redirect('/playersPage')

            #New Room Creation
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


        #Handles request to enter in a room
        elif 'enter_room' in request.POST:
            user = request.user

            #If the player is already in another room, redirect to old room
            if Player.objects.filter(player=user).exists():
                player = Player.objects.get(player=user)
                room = player.in_room
                messages.warning(request,f'You\'re already in the room {room.room_code}. Please leave this room first.')
                return redirect('/playersPage')

            admin_user = False
            room_code = request.POST.get('room_code')

            #Add player to the room, also check for full room
            if Room.objects.filter(room_code=room_code).exists():
                room = Room.objects.get(room_code=room_code)
                if room.currentPlayersCount >=4:
                    messages.warning(request, 'Sorry! This room is full.')
                    return redirect('/room')
                player1 = request.user
                addPlayer(player=player1, room=room)
                
            #If wrong room code is entered
            else:
                messages.info(request, 'This room doesn\'t exist')
                return redirect('/enterRoom')

    else:
        #If anonymous user(who is not in any room) tries to access players page, then redirect to /room
        user = request.user
        if Player.objects.filter(player=user).exists():
            player = Player.objects.get(player=user)
            room = player.in_room
            if request.user.username == room.room_admin:
                admin_user = True
            else:
                admin_user = False
        else:
            messages.warning(request, 'Please Create or join a room first.')
            return redirect('/room')


    #Prepare Player list to pass in the playersPage
    players_list = []
    player_node = room.head
    player_node.save()
    while player_node is not None:
        username = player_node.player.username
        name = player_node.player.first_name + " " + player_node.player.last_name
        players_list.append((username,name))
        player_node = player_node.next
        if player_node is not None:
            player_node.save()


    context= {
        'roomCode': room.room_code,
        'players' : players_list,
        'loginStatus': loginStatus,
        'roomAdmin': room.room_admin,
        'admin_user': admin_user,
    }
    return render(request, 'players.html', context)






#To handle Logout request
def logoutUser(request):
    logout(request)
    return redirect('/')





#About Page
def about(request):
    loginStatus = True
    if request.user.is_anonymous:
        loginStatus = False
    context = {'loginStatus' : loginStatus}
    return render(request, 'about.html', context)
    





#IDE
def ide(request):
    if request.user.is_anonymous:
        context = {'loginStatus' : False}
        return render(request, 'register.html', context)
        
    if request.method=="POST":
        #Get all request Information
        room_code = request.POST.get('room_code')
        room = Room.objects.get(room_code=room_code)
        no_of_questions = int(room.no_of_questions)


        #Prepare a players list to pass in IDE leaderboard
        players_list = []
        player_node = room.head
        player_node.save()
        while player_node is not None:
            username = player_node.player.username
            name = player_node.player.first_name + " " + player_node.player.last_name
            score = player_node.score
            players_list.append((username,name,score))
            player_node = player_node.next
            if player_node is not None:
                player_node.save()

        context = {
            'no_of_questions':range(1,no_of_questions+1),
            'players': players_list,
            'roomCode': room_code,
            'result': "",
            'error': "",
            'bufferCode': "#include<iostream> \nusing namespace std; \nint main() \n{\n cout<<\"Hello C++\";\n return 0;\n}\n",
            'language' : "c++"
        }

        return render(request, 'ide.html', context)

    #If anyone directly tries to access /ide, redirect to playersPage or Sign-In page
    else:
        return redirect('/playersPage')








#To execute the IDE Code
#This funtion is very much identical to 'ide' function, it is just capable to execute the code.
def executeCode(request):
    if request.user.is_anonymous:
        context = {'loginStatus' : False}
        return render(request, 'register.html', context)
        
    if request.method=="POST":
        room_code = request.POST.get('room_code')
        room = Room.objects.get(room_code=room_code)
        no_of_questions = int(room.no_of_questions)

        players_list = []
        player_node = room.head
        player_node.save()
        while player_node is not None:
            username = player_node.player.username
            name = player_node.player.first_name + " " + player_node.player.last_name
            score = player_node.score
            players_list.append((username,name,score))
            player_node = player_node.next
            if player_node is not None:
                player_node.save()

        language = request.POST.get('language')
        bufferCode = request.POST.get('bufferCode')

        if language == "python":
            result, error = executeUserPythonCode(bufferCode)
        elif language == "java":
            result, error = executeUserJavaCode(bufferCode)
        elif language == "c++":
            result, error = executeUserCPPCode(bufferCode)
        else:
            result, error = None, None
        if result is not None:
            result = result.splitlines()
        else:
            result = []
        if error is not None:
            error = error.splitlines()
        else:
            error = []

        context = {
            'no_of_questions':range(1,no_of_questions+1),
            'players': players_list,
            'roomCode': room_code,
            'result': result,
            'error': error,
            'bufferCode': bufferCode,
            'language': language,
        }

        return render(request, 'ide.html', context)

    else:
        return redirect('/playersPage')



