from django.contrib import messages
from django.contrib.auth.models import User
from django.http import JsonResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, redirect
from workspace.models import Workspace


def add(request):
    if request.method == "POST":
        owner = request.user
        workspace = request.POST.get("workspace")
        member = request.POST.get("member")
        workspace_filtered = Workspace.objects.filter(name=workspace)
        list_of_workspace = list(workspace_filtered)
        if member == owner.username:
            messages.info(request, 'Owner cannot be added twice.')
            return HttpResponseRedirect('/member/add')
        if len(list_of_workspace) == 0:
            messages.info(request, 'Workspace does not exist.')
            return HttpResponseRedirect('/member/add')
        else:
            workspace_filtered = workspace_filtered.filter(owner=owner)
            list_of_workspace = list(workspace_filtered)
            if len(list_of_workspace) == 0:
                messages.info(request, 'Workspace exists, but you do not have authority to access.')
                return HttpResponseRedirect('/member/add')
            else:
                workspace_to_add = Workspace.objects.get(owner=owner, name=workspace)
                try:
                    member_to_add = User.objects.get(username=member)
                except User.DoesNotExist:
                    member_to_add = None
                if member_to_add is not None:
                    if not list(workspace_to_add.member.filter(username=member)):
                        if len(list(workspace_to_add.member.all())) >= 10:
                            messages.info(request, 'You cannot add more then 10 people.')
                            return HttpResponseRedirect('/member/add')
                        workspace_to_add.member.add(member_to_add)
                        messages.info(request, 'Successfully added [' + member + '] member to your workspace.')
                        return HttpResponseRedirect('/member/add')
                    else:
                        messages.info(request, 'Already member added.')
                        return HttpResponseRedirect('/member/add')
                else:
                    messages.info(request, 'Username does not exist.')
                    return HttpResponseRedirect('/member/add')
    else:
        if not request.user.is_authenticated:
            return redirect('/user/signin')
        return render(request, 'member/add.html', {})


def delete(request):
    if request.method == "POST":
        owner = request.user
        workspace = request.POST.get("workspace")
        member = request.POST.get("member")
        workspace_filtered = Workspace.objects.filter(name=workspace)
        list_of_workspace = list(workspace_filtered)
        if member == owner.username:
            messages.info(request, 'Owner cannot be deleted.')
            return HttpResponseRedirect('/member/delete')
        if len(list_of_workspace) == 0:
            messages.info(request, 'Workspace does not exist.')
            return HttpResponseRedirect('/member/delete')
        else:
            workspace_filtered = workspace_filtered.filter(owner=owner)
            list_of_workspace = list(workspace_filtered)
            if len(list_of_workspace) == 0:
                messages.info(request, 'Workspace exists, but you do not have authority to access.')
                return HttpResponseRedirect('/member/delete')
            else:
                workspace_to_add = Workspace.objects.get(owner=owner, name=workspace)
                try:
                    member_to_del = User.objects.get(username=member)
                except User.DoesNotExist:
                    member_to_del = None
                if member_to_del is not None:
                    if list(workspace_to_add.member.filter(username=member)):
                        workspace_to_add.member.remove(member_to_del)
                        messages.info(request, 'Successfully removed [' + member + '] member to your workspace.')
                        return HttpResponseRedirect('/member/add')
                    else:
                        messages.info(request, 'Already member deleted.')
                        return HttpResponseRedirect('/member/add')
                else:
                    messages.info(request, 'Username does not exist.')
                    return HttpResponseRedirect('/member/delete')
    else:
        if not request.user.is_authenticated:
            return redirect('/user/signin')
        return render(request, 'member/delete.html', {})


def get(request):
    if request.method == "POST":
        owner = request.user
        workspace = request.POST.get("workspace")
        workspace_filtered = Workspace.objects.filter(name=workspace)
        list_of_workspace = list(workspace_filtered)
        if len(list_of_workspace) == 0:
            messages.info(request, 'Workspace does not exist.')
            return HttpResponseRedirect('/member/get')
        else:
            workspace_filtered = workspace_filtered.filter(owner=owner)
            list_of_workspace = list(workspace_filtered)
            if len(list_of_workspace) == 0:
                messages.info(request, 'Workspace exists, but you do not have authority to access.')
                return HttpResponseRedirect('/member/get')
            else:
                workspace_to_look = Workspace.objects.get(owner=owner, name=workspace)
                user_list = list(workspace_to_look.member.all())
                messages.info(request, 'OWNER::' + owner.username)
                for element in user_list:
                    messages.info(request, 'MEMBER::' + element.username)
                return HttpResponseRedirect('/member/list')

    else:
        if not request.user.is_authenticated:
            return redirect('/user/signin')
        return render(request, 'member/get.html', {})


def list_member(request):
    return render(request, 'member/list.html', {})
