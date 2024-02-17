""" imports """
from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from .models import UserAccount


User = get_user_model()

class UserAccountModelSerializer(serializers.ModelSerializer):
    """
    Serializer for UserAccount model.
    """

    class Meta:
        model = UserAccount
        fields = ("username", "password", "email", "phone_number")

    def validate(self, data):
        """ Validate password """
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
        """
        Create new user.
        """
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            phone_number=validated_data["phone_number"],
            password=validated_data["password"],
        )
        return user


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for UserAccount model.
    """

    class Meta:
        model = UserAccount
        fields = ("username", "email", "phone_number")


class ProfileImageSerializer(serializers.ModelSerializer):
    """
    Serializer for updating profile image.
    """

    class Meta:
        model = UserAccount
        fields = ("image",)
