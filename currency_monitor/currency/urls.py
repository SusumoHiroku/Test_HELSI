from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CurrencyViewSet, RateViewSet

router = DefaultRouter()
router.register(r'currencies', CurrencyViewSet, basename='currency')
router.register(r'rates', RateViewSet, basename='rate')

urlpatterns = [
    path('', include(router.urls)),
]
