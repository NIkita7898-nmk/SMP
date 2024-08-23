from django.urls import path

from user.views import (
    UserCreateViewset,
    CustomTokenObtainPairView,
    ChangePassword,
    LogoutView,
    SearchView,
)

urlpatterns = [
    path(
        "create/", UserCreateViewset.as_view({"post": "create"}), name="create-account"
    ),
    path("login/", CustomTokenObtainPairView.as_view(), name="login"),
    path(
        "update-user/<int:pk>/",
        UserCreateViewset.as_view({"put": "update"}),
        name="update-user",
    ),
    path("change-password/", ChangePassword.as_view(), name="update-user"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("search/", SearchView.as_view(), name="search"),
]
