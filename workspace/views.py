from django.contrib import messages
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from workspace.models import Workspace


def main(request):
    return render(request, 'workspace/main.html')


def index(request):
    if not request.user.is_authenticated:
        return redirect('/user/signup')
    return render(request, 'workspace/insert.html', {})


def insert(request):
    if request.method == "POST":
        which_user = request.user
        name = request.POST.get("name")
        workspace_filtered = Workspace.objects.filter(owner=which_user, name=name)
        list_of_workspace = list(workspace_filtered)
        if len(list_of_workspace) != 0:
            messages.info(request, 'This name of workspace is already made by you.')
            return HttpResponseRedirect('/workspace/insert')
        else:
            workspace_filtered = Workspace.objects.filter(owner=which_user)
            list_of_workspace = list(workspace_filtered)
            if len(list_of_workspace) >= 5:
                messages.info(request, 'You have too many workspaces. You already have 5 workspaces.')
                return HttpResponseRedirect('/workspace/main')
            else:
                if len(name) > 500:
                    messages.info(request, 'The name of your workspace is too long. Try shorter.')
                    return HttpResponseRedirect('/workspace/insert')
                Workspace.objects.create(owner=which_user, name=name)
                messages.info(request, 'Successfully made your own workspace with name [' + str(name) + '].')
                return HttpResponseRedirect('/workspace/main')
    else:
        if not request.user.is_authenticated:
            return redirect('/user/signin')
        return render(request, 'workspace/insert.html', {})


def update(request):
    if request.method == "POST":
        which_user = request.user
        old_name = request.POST.get("old_name")
        new_name = request.POST.get("new_name")
        workspace_filtered = Workspace.objects.filter(owner=which_user, name=old_name)
        list_of_workspace = list(workspace_filtered)
        workspace_filtered_new = Workspace.objects.filter(owner=which_user, name=new_name)
        list_of_workspace_new = list(workspace_filtered_new)
        if len(list_of_workspace_new) != 0:
            messages.info(request, 'This new name of workspace is already made by you.')
            return HttpResponseRedirect('/workspace/update')
        if len(list_of_workspace) == 0:
            messages.info(request, 'This name of workspace owned by you does not exist.')
            return HttpResponseRedirect('/workspace/update')
        else:
            if len(new_name) > 500:
                messages.info(request, 'The name of your workspace is too long. Try shorter.')
                return HttpResponseRedirect('/workspace/update')
            workspace_to_update = Workspace.objects.get(owner=which_user, name=old_name)
            workspace_to_update.name = new_name
            workspace_to_update.save()
            messages.info(request, 'Successfully changed your own '
                                   'workspace with name [' + str(old_name) + '] to name [' + str(new_name) + '].')
            return HttpResponseRedirect('/workspace/main')
    else:
        if not request.user.is_authenticated:
            return redirect('/user/signin')
        return render(request, 'workspace/update.html', {})