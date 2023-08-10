from django.urls import path

from .views import InviteDoneView, InvitePlateCheck

urlpatterns = [
    path('check/', InvitePlateCheck.as_view()),
    path("done/", InviteDoneView.as_view())
]
