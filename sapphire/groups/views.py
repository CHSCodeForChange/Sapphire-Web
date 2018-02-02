from django.shortcuts import render, redirect
from django.http import HttpResponse

from groups.models import Group
from groups.forms import NewGroupForm


# Create your views here.
def list(request):
    groups = Group.objects.order_by('hours')
    if request.user.is_authenticated():
        return render(request, 'groups/groupListView.html', {'groups': groups})
    else:
        return redirect('login')

def group(request):
    group = Group.objects.get(pk=group_id)
    return render(request, 'groups/groupView.html', {'group':group})

def add(request):
    if request.user.is_authenticated():
        if request.method == 'GET':
            form = NewGroupForm(owner=request.user)
        else:
            form = NewGroupForm(request.POST, owner=request.user)
            if form.is_valid():
                group = form.save(commit=False)
                group.save()

                return redirect("/groups/"+str(group.id))

        return render(request, 'groups/addGroup.html', {'form':form})

    else:
        return redirect('login')
