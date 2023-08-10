from django.urls import path
from marketplace.api.view import ProductView

urlpatterns = [
    path('product/', ProductView.as_view()),
]
