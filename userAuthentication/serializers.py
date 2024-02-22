""" imports """
from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core import exceptions
from django.core.exceptions import ValidationError
from .models import UserAccount

User = get_user_model()

class UserAccountModelSerializer(serializers.ModelSerializer):
    """
    Serializer for UserAccount model.
    """

    class Meta:
        model = UserAccount
        fields = ("username", "password", "email", "phone_number", )

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
        fields = ("username", "email", "phone_number", "id" ,"password")


class ProfileImageSerializer(serializers.ModelSerializer):
    """
    Serializer for updating profile image.
    """

    class Meta:
        model = UserAccount
        fields = ("image",)
        

class UpdateUserProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for updating user profile.
    """
    
    class Meta:
        model = UserAccount
        fields = ("username", "password", "phone_number", "email")

    def validate_password(self, value):
        """ Validate password """
        user = self.instance
        try:
            validate_password(value, user)
        except ValidationError as e:
            raise serializers.ValidationError({"password": e.messages})
        return value

    def validate(self, data):
        """ Validate data """
        existing_data = UserAccount.objects.filter(email=data.get('email')).first()

        # If there's existing data, fill in None fields with existing data
        if existing_data:
            for field in data:
                if data[field] is None:
                    print(f"Field '{field}' is None. Filling with existing data: {getattr(existing_data, field)}")
                    data[field] = getattr(existing_data, field)

        # Validate and handle password and phone_number fields
        if "password" in data:
            if data["password"].strip() == "":
                print("Password field is empty. Removing it.")
                del data["password"]  # Remove the password field if empty
            else:
                data["password"] = self.validate_password(data["password"])

        if "phone_number" in data:
            if data["phone_number"].strip() == "":
                print("Phone number field is empty. Removing it.")
                del data["phone_number"]  # Remove the phone_number field if empty
        
        return data

    def update(self, instance, validated_data):
        """
        Update existing user profile.
        """
        instance.username = validated_data.get("username", instance.username)
        instance.phone_number = validated_data.get("phone_number", instance.phone_number)
        instance.email = validated_data.get("email", instance.email)

        # Update password only if provided
        if "password" in validated_data:
            print("Updating password.")
            instance.set_password(validated_data["password"])

        instance.save()
        return instance


class PasswordSerializers(serializers.ModelSerializer):
    class Meta:
        model = UserAccount
        fields = ['id', 'username', 'password', 'email', 'phone_number']

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = UserAccount.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        if 'password' in validated_data:
            password = validated_data.pop('password')
            instance.set_password(password)
        return super().update(instance, validated_data)