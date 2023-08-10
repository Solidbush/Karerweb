from rest_framework.generics import GenericAPIView
from marketplace.api.serializers import ProductSerializer
from marketplace.models import Product
from rest_framework.response import Response

class ProductView(GenericAPIView):
    def get(self, request):
        products = Product.objects.all()
        return Response(ProductSerializer(products, many=True).data)