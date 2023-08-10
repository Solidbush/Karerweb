from rest_framework.viewsets import ModelViewSet

from ..models import History
from .serializers import HistorySerializer


class HistoryView(ModelViewSet):
    http_method_names = ['get', 'post']
    queryset = History.objects.all()
    serializer_class = HistorySerializer
