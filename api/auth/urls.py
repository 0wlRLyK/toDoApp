from django.urls import path
# fmt: off
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

# fmt: on

app_name = "auth"
urlpatterns = [
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
