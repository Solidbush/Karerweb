from django.urls import path

from .views import InviteDoneView, InvitePlateCheck, LegalEntityStatement

urlpatterns = [
    path('check/', InvitePlateCheck.as_view()),
    path("done/", InviteDoneView.as_view()),
    path("lega_entity_statement/", LegalEntityStatement.as_view())
]
