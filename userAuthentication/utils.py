from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    
    """
    Custom token serializer to include additional payload data.
    
    Inherits from TokenObtainPairSerializer and overrides the get_token method
    to add custom payload data such as username and phone number to the token.
    """

    @classmethod
    def get_token(cls, user):
        """
        Override the get_token method to add custom payload data to the token.

        Args:
            user: The user object for which the token is being generated.

        Returns:
            token: The JWT token with custom payload data.
        """
        token = super().get_token(user)

        # Add custom payload data to the token
        token['username'] = user.username
        token['phone_number'] = user.phone_number
        token['email'] = user.email
        token['image'] = user.image.url if user.image else None
        token['is_superuser'] = user.is_superuser

        return token
