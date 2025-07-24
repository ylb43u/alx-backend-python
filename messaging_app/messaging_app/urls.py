from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from chats.views import UserViewSet
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

router = DefaultRouter()
router.register(r'users', UserViewSet)

urlpatterns = [
    path("admin/", admin.site.urls),
    path('api/', include('chats.urls')),
    path('api-auth/', include('rest_framework.urls')),  # Optional: for browsable API login/logout

    # 🔐 JWT Authentication Endpoints:
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    path('api/', include(router.urls)),
]
