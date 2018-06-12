from django.shortcuts import render, redirect
from django.http import HttpResponse

from groups.models import Group, Chat_Entry
from utility.models import Event
from groups.forms import NewGroupForm, NewChatEntryForm, EditGroupForm, SearchGroupsForm
from django.contrib.auth.models import User
from alerts.models import Alert
from utility.models import *
from feed.models import Feed_Entry



# Create your views here.
def list(request):
    groups = Group.objects.order_by('hours')

    if request.method == 'GET':
        form = SearchGroupsForm()
    else:
        form = SearchGroupsForm(request.POST)
        if form.is_valid():
            groups = form.save(commit=False)
        return render(request, 'groups/groupListView.html', {'groups': groups, 'form': form})

    if request.user.is_authenticated():
        return render(request, 'groups/groupListView.html', {'groups': groups, 'form': form})
    else:
        return redirect('login')

def console(request, group_id):
    group = Group.objects.get(id=group_id)
    if request.user.is_authenticated():
        if group.get_is_organzer(request.user):
            user_slots = User_Slot.getUserSlots(group)
            feed_entries = Feed_Entry.objects.filter(group=group).order_by('-datetime')[:10]
            return render(request, 'groups/console.html', {'group':group, 'user_slots':user_slots, 'feed_entries':feed_entries})
        else:
            return redirect('/groups/'+str(group_id))
    else:
        return redirect('login')

def update(request, group_id):
    group = Group.objects.get(id=group_id)
    owner = group.owner
    if request.user.is_authenticated():
        form = EditGroupForm(request.POST, id=group_id)
        if form.is_valid():
            data = form.save(commit=False)
            group.name = data['name']
            group.tagline = data['tagline']
            group.description = data['description']
            group.email = data['email']
            group.website = data['website']
            group.location = data['location']
            group.address = data['address']
            group.city = data['city']
            group.state = data['state']
            group.zip_code = data['zip_code']
            group.approvalNeeded = data['approvalNeeded']
            group.private = data['private']

            group.save()

            alert = Alert(user=request.user, text="Updated group "+group.name, color=Alert.getBlue())
            alert.saveIP(request)

            return redirect("/groups/"+str(group.id))

    form = EditGroupForm(id=group_id, initial={'name':group.name, 'tagline':group.tagline, 'description':group.description,
    'email':group.email, 'website':group.website, 'location':group.location, 'address':group.address, 'city':group.city,
    'state':group.state, 'zip_code':group.zip_code, 'approvalNeeded': group.approvalNeeded, 'private': group.private})

    return render(request, 'groups/editGroup.html', {'form':form})

def group(request, group_id):
    group = Group.objects.get(id=group_id)
    events = Event.objects.filter(parentGroup=group)
    is_owner = group.owner == request.user
    return render(request, 'groups/groupView.html', {'group':group, 'events':events,
        'is_member':group.get_is_member(request.user), 'is_owner':is_owner, 'is_organizer':group.get_is_organzer(request.user)})

def join(request, group_id):
    group = Group.objects.get(id=group_id)
    if (group.get_is_member(request.user) == False):
        if (group.approvalNeeded):
            group.pendingUsers.add(request.user)
            group.save()

            alert = Alert(user=request.user, text="Requested to join "+str(group.name)+", wating for organizer approval", color=Alert.getGreen())
            alert.saveIP(request)

        else:
            group.volunteers.add(request.user)
            group.save()

            alert = Alert(user=request.user, text="Joined "+str(group.name), color=Alert.getGreen())
            alert.saveIP(request)

    return redirect('/groups/'+str(group_id))

def approve(request, group_id, user_id):
    group = Group.objects.get(id=group_id)
    user = User.objects.get(id=user_id)
    if (group.get_is_organzer(request.user) and group.get_is_pending(user)):
        group.pendingUsers.remove(user)
        group.volunteers.add(user)
        group.save()

        alert = Alert(user=request.user, text=user.username+" is now a volunteer", color=Alert.getYellow())
        alert.saveIP(request)
    else:
        if (not(group.get_is_organzer(request.user))):
            alert = Alert(user=request.user, text="Only organizers or owners can approve pending users", color=Alert.getRed())
            alert.saveIP(request)
        else:
            alert = Alert(user=request.user, text="This is not a pending user", color=Alert.getRed())
            alert.saveIP(request)

    return redirect('/groups/'+str(group_id))




def leave(request, group_id):
    group = Group.objects.get(id=group_id)
    if (group.get_is_organzer(request.user) and group.get_is_owner(request.user) == False ):
        group.organizers.remove(request.user)
        group.save()
    if (group.get_is_member(request.user)):
        group.volunteers.remove(request.user)
        group.save()
    if (group.get_is_owner(request.user)):
        return render(request, "groups/pickNewOwner.html", {"organizers":group.organizers.all()})

    alert = Alert(user=request.user, text="Left "+str(group.name), color=Alert.getRed())
    alert.saveIP(request)

    return redirect('/groups/'+str(group_id))

def pickNewOwner(request, group_id, new_owner_id):
    group = Group.objects.get(id=group_id)
    user = User.objects.get(id=new_owner_id)
    if (group.owner == request.user and group.get_is_organzer(user)):
        group.organizers.remove(user)
        group.owner = user
        group.save()

        alert = Alert(user=request.user, text="Left "+str(group.name), color=Alert.getRed())
        alert.saveIP(request)
    else:
        if (not(group.get_is_organzer(user))):
            alert = Alert(user=request.user, text="The new owner must be a current organizer", color=Alert.getRed())
            alert.saveIP(request)
        else:
            alert = Alert(user=request.user, text="You must be the owner", color=Alert.getRed())
            alert.saveIP(request)
    return redirect('/groups/'+str(group_id))


def changePermissionLevel(request, group_id, user_id):
    user = User.objects.get(id=user_id)
    group = Group.objects.get(id=group_id)
    if (request.user != group.owner):
        alert = Alert(user=request.user, text=user.name+" is now a "+group.get_role(user), color=Alert.getRed())
        alert.saveIP(request)
        return redirect('/groups/'+str(group_id))

    for curr_user in group.volunteers.all():
        if (curr_user == user):
            group.volunteers.remove(user)
            group.organizers.add(user)
            group.save()

            alert = Alert(user=request.user, text=user.username+" is now an organizer", color=Alert.getYellow())
            alert.saveIP(request)

            return redirect('/groups/'+str(group_id))


    for curr_user in group.organizers.all():
        if (curr_user == user):
            group.organizers.remove(user)
            group.volunteers.add(user)
            group.save()

            alert = Alert(user=request.user, text=user.username+" is now a volunteer", color=Alert.getYellow())
            alert.saveIP(request)
            return redirect('/groups/'+str(group_id))
    return redirect('/groups/'+str(group_id))



def add(request):
    if request.user.is_authenticated():
        if request.method == 'GET':
            form = NewGroupForm(owner=request.user)
        else:
            form = NewGroupForm(request.POST, owner=request.user)
            if form.is_valid():
                group = form.save(commit=False)
                group.save()

                alert = Alert(user=request.user, text="Created group "+group.name, color=Alert.getBlue())
                alert.saveIP(request)

                return redirect("/groups/"+str(group.id))

        return render(request, 'groups/addGroup.html', {'form':form})

    else:
        return redirect('login')

def chat(request, group_id):
    group = Group.objects.get(id=group_id)

    if not Group.get_is_member(group, request.user):
        return HttpResponse('You don\'t have the right permissions to see this page. You must be a member to access this page.')

    chat_entries = Chat_Entry.objects.filter(parentGroup=group).order_by('datetime')
    if(request.method == 'POST'):
        form = NewChatEntryForm(request.POST, user=request.user, parentGroup=group)
        if form.is_valid():
            chat = form.save(commit=False)
            chat.save()

            return redirect('/groups/'+str(group_id)+'/chat/')

    else:
        form = NewChatEntryForm(user=request.user, parentGroup=group)

    # Filter this by single slot events in the future
    return render(request, 'groups/chat.html', {'entries':chat_entries, 'form':form})
