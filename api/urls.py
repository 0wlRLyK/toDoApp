from django.urls import include, path

app_name = "api"

urlpatterns = [path("auth/", include("api.auth.urls"))]
