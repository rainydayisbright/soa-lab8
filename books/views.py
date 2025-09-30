from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework import viewsets, mixins

from .models import Book
from .serializers import BookSerializer

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['author', 'is_available']
    search_fields = ['title', 'author']
    ordering_fields = ['title', 'published_date', 'price']
    ordering = ['-published_date']

    @action(detail=False, methods=['get'])
    def available_books(self, request):
        available_books = Book.objects.filter(is_available=True)
        serializer = self.get_serializer(available_books, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def toggle_availability(self, request, pk=None):
        book = self.get_object()
        book.is_available = not book.is_available
        book.save()
        return Response({
            'id': book.id,
            'title': book.title,
            'is_available': book.is_available,
            'message': f'สถานะการใช้งานของ "{book.title}" ถูกเปลี่ยนเป้น {book.is_available}'
        })
    
    @action(detail=False, methods=['get'], url_path='author/(?P<author_name>[^/.]+)')
    def books_by_author(self, request, author_name=None):
        books = Book.objects.filter(author__icontains=author_name)
        serializer = self.get_serializer(books, many=True)
        return Response(serializer.data)
    
class BookReadOnlyViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = [SearchFilter]
    search_fields = ['title', 'author']

class BookCustomViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    viewsets.GenericViewSet
):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
