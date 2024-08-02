
from email import message
from os import name
from django.shortcuts import render, redirect, get_object_or_404
from chat.models import Room, Message, UserStatus
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_GET
from django.contrib.auth.models import User, auth
from django.contrib.auth import authenticate, login, logout as auth_logout
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.core.validators import validate_slug
from django.contrib.auth import logout as logouts

# Create your views here.
def home(request):
    return render(request, 'home.html')

def room(request, room):
    username = request.GET.get('username')
    room_details = Room.objects.get(name=room)
    return render(request, 'room.html', {'username':username, 'room':room, 'room_details':room_details})

def checkview(request):
    if request.method == 'POST':
        room = request.POST.get('room_name')
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not Room.objects.filter(name=room).exists():
            new_room = Room.objects.create(name=room)
            new_room.save()
        if not User.objects.filter(username=username).exists():
            messages.error(request, "Username does not exist.")
            return redirect('home') 
        user = authenticate(username=username, password=password)
        if user is None:
            messages.error(request, "Invalid username or password.")
            return redirect('home')
        login(request, user)
        return redirect(f'/{room}/?username={username}')
    return render(request, 'home.html')



def send(request):
    message = request.POST['message']
    username = request.POST['username']
    room_id = request.POST['room_id']

    new_message = Message.objects.create(value=message, user=username, room=room_id)
    new_message.save()
    return HttpResponse('Message sent successfully')


def getMessages(request, room):
    room_details = Room.objects.get(name=room)

    messages = Message.objects.filter(room=room_details.id)
    return JsonResponse({"messages":list(messages.values())})



def create(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')

        if not username or not password or not password2:
            messages.error(request, "All fields are required.")
            return redirect('create')

        if password != password2:
            messages.error(request, "Passwords do not match.")
            return redirect('create')

        if User.objects.filter(username=username).exists():
            messages.info(request, "Username already exists.")
            return redirect('create')

        try:
            validate_slug(username)
            user = User.objects.create_user(username=username, password=password)
            user.save()
            messages.success(request, "User created successfully.")
            return redirect('home')
        except ValidationError:
            messages.error(request, "Invalid username format.")
            return redirect('create')
    else:
        return render(request, 'create.html')
    
def logout(request):
    logouts(request)
    return redirect('/')


def chat_room(request, room_name):
    room = get_object_or_404(Room, name=room_name)
    UserStatus.objects.update_or_create(
        user=request.user,
        room=room,
        defaults={'is_online': True}
    )
    users = UserStatus.objects.filter(room=room, is_online=True)
    return render(request, 'room.html', {'room': room, 'users': users})