from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Product
from .serializers import ProductSerializer
from django_filters.rest_framework import DjangoFilterBackend

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    filter_backends = [DjangoFilterBackend]

    filterset_fields = ['category', 'is_active', 'stock', 'price']

    @action(detail=False, methods=['get'])
    def in_stock(self, request):
        products = Product.objects.filter(stock__gt=0)
        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def toggle_active(self, request, pk=None):
        product = self.get_object()
        old_status = product.is_active
        product.is_active = not product.is_active
        product.save()
        print(f"Toggled product {product.id} from {old_status} to {product.is_active}")
        return Response({'status': 'updated', 'is_active': product.is_active})


    @action(detail=False, methods=['get'], url_path='category/(?P<category_name>[^/.]+)')
    def by_category(self, request, category_name=None):
        products = Product.objects.filter(category__iexact=category_name)
        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data)
