from django.contrib.auth import logout
from django.db.models import Q

from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView

from user.models import CustomUser
from rest_framework.exceptions import PermissionDenied
from user.serializer import (
    UserSerializer,
    CustomTokenObtainPairSerializer,
    ChangePasswordSerializer,
)
from utils.token import UserMixin


# Create your views here.
class UserCreateViewset(viewsets.ModelViewSet):

    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]
    lookup_field = "pk"

    def get_object(self):
        obj = super().get_object()

        # Check if the logged-in user is trying to access their own profile
        if obj != self.request.user:
            raise PermissionDenied(
                "You do not have permission to edit this user's profile."
            )
        return obj

    def get_queryset(self):
        return CustomUser.objects.filter(id=self.request.user.id)


class ChangePassword(UserMixin, APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            response_data = serializer.update(request.user, serializer.validated_data)
            return Response(response_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class LogoutView(APIView):

    def get(self, request):
        logout(request)
        return Response(
            {"detail": "Successfully logged out."}, status=status.HTTP_200_OK
        )


class SearchView(APIView):

    def get(self, request):
        search_obj = request.query_params.get("data")
        print(search_obj)
        user = CustomUser.objects.filter(
            Q(first_name__contains=search_obj)
            | Q(last_name__contains=search_obj)
            | Q(email__contains=search_obj)
        )
        print(user)
        serializer = UserSerializer(user, many=True)
        if serializer.is_valid:

            return Response(serializer.data)
