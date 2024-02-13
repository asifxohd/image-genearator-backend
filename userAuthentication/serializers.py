from rest_framework import serializers
from .models import UserAccount
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError


User = get_user_model()

class UserAccountModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAccount
        fields = ("username", "password", "email", "phone_number")

    def validate(self, data):
        password = data.get("password")
        user = User(**data)

        try:
            validate_password(password, user)
        except ValidationError as e:
            serializers_error = serializers.as_serializer_error(e)
            raise ValidationError(
                {
                    "password": serializers_error["non_field_errors"],
                }
            )

        return data

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            phone_number=validated_data["phone_number"],
            password=validated_data["password"],
        )
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAccount
        fields = ("username", "email", "phone_number")
