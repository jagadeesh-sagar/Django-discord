from django.shortcuts import render,redirect
from django.db.models import Q
from django.http import HttpResponse
from .models import Room,Topic,Message
from .forms import RoomForm,MessageForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate #authenticate is also often useful
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm


def home(request):
  q=request.GET.get('q') if request.GET.get('q') != None else ''
  rooms=Room.objects.filter(
                            Q(topic__name__icontains=q) | Q(name__icontains=q)| Q(description__icontains=q))
  topics=Topic.objects.all()
  room_count=rooms.count

  return render(request,'base/home.html',{'rooms':rooms,'topics':topics,'room_count':room_count})


def room(request,pk):
  room=Room.objects.get(id=pk)  
  room_messages=room.message_set.all()
  
  if request.method=="POST":
        Message.objects.create(
          user=request.user,
          room=room,
          body=request.POST.get('body')
      )
  context={'room':room,'room_messages':room_messages}
  return render(request,'base/room.html',context)
  # this gives all the children elements of message class which has primary key of room class 
  # form=MessageForm()
  # if request.method == 'POST':
  #       form = MessageForm(request.POST)

  #       if form.is_valid():
  #         message = form.save(commit=False) # Create message object but don't save yet
  #         message.user = request.user  # Set the user field
  #         message.room = room       # Set the room field
  #         message.save()
  #         return redirect('room', pk=room.id)


@login_required(login_url='login')
def createRoom(request):
  form = RoomForm()
  if request.method=="POST":
    form=RoomForm(request.POST)
    if form.is_valid():
     form.save()
     return redirect('home')

  context={'form':form}
  return render(request,'base/room_form.html',context)


@login_required(login_url='login')
def updateRoom(request,pk):
   room=Room.objects.get(id=pk)
   form=RoomForm(instance=room)

   if request.user!=room.host:
     return HttpResponse('your are not allowed here!')
   
   if request.method=="POST":
     form=RoomForm(request.POST, instance=room)
     if form.is_valid():
       form.save()
       return redirect('home')
   context={'form':form}

   return render(request,'base/room_form.html',context)


@login_required(login_url='login')
def deleteRoom(request,pk):
    room=Room.objects.get(id=pk)

    if request.user!=room.host:
     return HttpResponse('your are not allowed here!')

    if request.method=="POST":
      room.delete()
      return redirect('home')
    
    return render(request,'base/delete.html',{'obj':room})
  

def loginPage(request):
  page='login'
  if request.user.is_authenticated:
    return redirect('home')
  
  if request.method=="POST":
    username=request.POST.get('username').lower()
    password=request.POST.get('password')
       
    user=authenticate(request,username=username,password=password)
    if user is not None:
      # auth.login(request,user)
      login(request,user)
      return redirect('home')
    else:
      messages.error(request,'Username or password does not exit')

  context={'page':page}
  return render(request,'base/login_register.html',context)


def registerPage(request):
  form=UserCreationForm()
  if request.method =="POST":
    form=UserCreationForm(request.POST)
    if form.is_valid(): 
      user=form.save(commit=False)
      user.username=user.username.lower()
      user.save()
      login(request,user)
      return redirect('home')
    else:
      messages.error(request,'An error occured during registration')
  return render(request,'base/login_register.html',{"form":form})

def logoutUser(request):
  logout(request)
  return redirect('home')