from django.shortcuts import render,redirect
from django.db.models import Q
from django.http import HttpResponse
from .models import Room,Topic,Message
from .forms import RoomForm,MessageForm,UserForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate #authenticate is also often useful
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm


def home(request):
  q=request.GET.get('q') if request.GET.get('q') != None else ''
  rooms=Room.objects.filter(
                              Q(topic__name__icontains=q) | Q(name__icontains=q)| Q(description__icontains=q))

  topics=Topic.objects.all()[0:2]
  room_count=rooms.count()
  room_messages=Message.objects.filter(Q(room__topic__name__icontains=q))

  return render(request,'base/home.html',{'rooms':rooms,'topics':topics,'room_count':room_count,'room_messages':room_messages})


def room(request,pk):
  room=Room.objects.get(id=pk)  
  room_messages=room.message_set.all()
  participants=room.participants.all()
  
  if request.method=="POST":
        Message.objects.create(
          user=request.user,
          room=room,
          body=request.POST.get('body')
      )
        room.participants.add(request.user)
        return redirect('room',pk=room.id)
  context={'room':room,'room_messages':room_messages,"participants":participants}
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


def userProfile(request,pk):
  user=User.objects.get(id=pk)
  rooms=user.room_set.all()
  room_messages=user.message_set.all()
  # room_messages = Message.objects.filter(user=user) 
  topics=Topic.objects.all()
  context={'user':user,'rooms':rooms,"room_messages":room_messages,"topics":topics}
  return render(request,'base/profile.html',context)


@login_required(login_url='login')
def createRoom(request):
  form = RoomForm()
  topics=Topic.objects.all()
  if request.method=="POST":
    form=RoomForm(request.POST)
    if form.is_valid():
     room=form.save(commit=False)
     room.host=request.user
     room.save()
     return redirect('home')
    else:
      print("not valid")

  context={'form':form ,'topics':topics}
  return render(request,'base/room_form.html',context)


@login_required(login_url='login')
def updateRoom(request,pk):
   room=Room.objects.get(id=pk)
   form=RoomForm(instance=room)
   topics=Topic.objects.all()

   if request.user!=room.host:
     return HttpResponse('your are not allowed here!')
   
   if request.method=="POST":
     form=RoomForm(request.POST, instance=room)
     if form.is_valid():
       form.save()
       return redirect('home')
   context={'form':form,'topics':topics}

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

@login_required(login_url='login')
def deleteMessage(request,pk):
    message=Message.objects.get(id=pk)

    if request.user!=message.user:
     return HttpResponse('your are not allowed here!')

    if request.method=="POST":
      message.delete()
      return redirect('home')
    
    return render(request,'base/delete.html',{'obj':message})


@login_required(login_url='login')
def updateUser(request):
  user=request.user
  form=UserForm(instance=user)
   
  if request.method=='POST':
   form=UserForm(request.POST,instance=user)
   if form.is_valid():
     form.save()
     return redirect('user-profile',pk=user.id)
  

  return render(request,'base/update-user.html',{'form':form})


def topicsPage(request):
  q=request.GET.get('q') if request.GET.get('q') != None else ''
  topics=Topic.objects.filter(name__icontains=q)
  return render(request,'base/topics.html',{"topics":topics})

def activityPage(request):
  room_messages=Message.objects.all()
  return render(request,'base/activity.html',{"room_messages":room_messages})