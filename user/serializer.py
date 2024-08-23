from django.contrib.auth import authenticate

from rest_framework import serializers, exceptions
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response

from user.models import CustomUser
from utils.token import UserMixin


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ("email", "first_name", "last_name", "password")
        extra_kwargs = {
            "password": {"write_only": True, "required": False},
            "email": {"required": False},
        }

    def create(self, validated_data):
        if "email" not in validated_data or "password" not in validated_data:
            raise exceptions.ValidationError("email and password are required.")

        user = CustomUser.objects.create_user(
            email=validated_data["email"],
            password=validated_data["password"],
            first_name=validated_data.get("first_name", ""),
            last_name=validated_data.get("last_name", ""),
            is_active=validated_data.get("is_active", True),
            is_staff=validated_data.get("is_staff", False),
        )
        return user

    def update(self, instance, validated_data):

        if "first_name" in validated_data:
            instance.first_name = validated_data["first_name"]
        if "last_name" in validated_data:
            instance.last_login = validated_data["last_name"]
        instance.save()
        return instance


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = "email"

    def validate(self, attrs):
        credentials = {"email": attrs.get("email"), "password": attrs.get("password")}
        user = authenticate(**credentials)

        if user:
            if not user.is_active:
                raise exceptions.AuthenticationFailed("User is deactivated")

            data = {}
            refresh = RefreshToken.for_user(user)

            data = {
                "access": str(refresh.access_token),
                "refresh": str(refresh),
            }
            return data
        else:
            raise exceptions.AuthenticationFailed(
                "No active account found with the given credentials"
            )


class ChangePasswordSerializer(serializers.Serializer):
    password = serializers.CharField(write_only=True)

    def update(self, instance, validated_data):
        try:
            if "password" in validated_data:
                instance.set_password(validated_data["password"])
                instance.save()
                return {"message": "Password updated successfully"}
            else:
                raise serializers.ValidationError("new_password is required")
        except Exception as e:
            raise serializers.ValidationError(str(e))
