from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api import views

app_name = 'api'

router_v1 = DefaultRouter()

router_v1.register(
    'categories',
    views.CategoryViewSet,
    basename='categories'
)
router_v1.register(
    'products',
    views.ProductViewSet,
    basename='products'
)

urlpatterns = [
    path('', include(router_v1.urls)),
    path('shopping_cart/', views.ShoppingCartAPIView.as_view()),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
