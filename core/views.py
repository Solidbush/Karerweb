import os

from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from . import forms

UserModel = get_user_model()


@csrf_exempt
def accept_pvc(request):
    email = request.POST.get("username", None)
    if not request.method == "POST":
        return HttpResponseRedirect("/")
    form = forms.SendPvcForm(request, request.POST)
    if not form.is_valid():
        errors = [str(value[0].message) for value in form.errors.as_data().values()]
        messages.add_message(request, messages.ERROR, str(". ".join(errors)))
        return HttpResponseRedirect(reverse("admin:login"))
    user, created = UserModel.objects.get_or_create(email=email)
    user.send_pvc()

    return render(request, "admin/accept_pvc.html", context={
        "title": "Войти",
        "form": forms.AdminAuthenticationForm(initial={"username": email})
    })


@csrf_exempt
def register(request):
    form = forms.RegisterSendPvcForm()
    if request.method == "POST":
        form = forms.RegisterSendPvcForm(request.POST)
        if form.is_valid():
            instance = form.save()
            try:
                instance.groups.add(Group.objects.get(id=os.getenv("CLIENT_GROUP_ID")))
            except Group.DoesNotExist:
                pass
            instance.send_pvc()
            return render(request, "admin/accept_pvc.html", context={
                "title": "Войти",
                "form": forms.AdminAuthenticationForm(initial={"username": instance.email})
            })
    return render(request, "admin/register.html", {
        "form": form
    })


@csrf_exempt
def register_accept_pvc(request):
    pass
