from rest_framework.routers import DefaultRouter

from apps.products.views import ProductViewSet, ProductPriceViewSet, ProductStatsViewSet

router = DefaultRouter()
router.register(r'products/prices', ProductPriceViewSet, basename='product-price')
router.register(r'products/stats', ProductStatsViewSet, basename='product-stats')
router.register(r'products', ProductViewSet, basename='product')

urlpatterns = router.urls
