from django.urls import path, include
from rest_framework.routers import SimpleRouter, DefaultRouter
from .views import BookViewSet, BookReadOnlyViewSet, BookCustomViewSet


router = SimpleRouter()

router.register(r'books', BookViewSet, basename='book')
router.register(r'book-reaonly', BookReadOnlyViewSet, basename='book-readonly')
router.register(r'book-custom', BookCustomViewSet, basename='book-custom')

urlpatterns = [
    path('api/', include(router.urls)),
]

# defaultrouter
router = DefaultRouter()
router.register(r'books', BookViewSet, basename='book')
router.register(r'book-readonly', BookReadOnlyViewSet, basename='book-readonly')

urlpatterns = [
    path('api/', include(router.urls)),
]

urlpatterns += router.urls
