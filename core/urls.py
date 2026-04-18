from django.contrib import admin
from django.urls import path
from django.http import JsonResponse
from finance.views import EmailLoginView

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from finance.views import RegisterView


def home(request):
    return JsonResponse({"message": "Budget AI Backend Running 🚀"})


urlpatterns = [
    path('', home),  # optional homepage
    path('admin/', admin.site.urls),

    # Auth
    path('api/register/', RegisterView.as_view(), name='register'),
    path('api/login/', EmailLoginView.as_view(), name='email_login'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
]