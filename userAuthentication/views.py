"""  imports  """
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from openai import OpenAI
from magic_words.settings import OPENAI_API_KEY
from django.contrib.auth import get_user_model
from .serializers import UserAccountModelSerializer, UserSerializer, ProfileImageSerializer


User = get_user_model()
class RegisterView(APIView):
    """
    API view to handle user registration.
    """

    def post(self, request):
        """
        Handle POST request to register a new user.

        Returns:
            Response: Response with user data if registration is successful,
                      otherwise returns validation errors.
        """
        serializer = UserAccountModelSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({'validation_errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        user = serializer.create(serializer.validated_data)
        user = UserSerializer(user)

        return Response(user.data, status=status.HTTP_201_CREATED)


class RetriveUserView(APIView):
    """
    API view to retrieve user information.
    """

    permissions_classes = [permissions.IsAuthenticated]

    def get(self, request):
        """
        Handle GET request to retrieve user information.

        Returns:
            Response: Response with user data if retrieval is successful.
        """
        user = UserSerializer(request.user)
        return Response(user.data, status=status.HTTP_200_OK)


class GenrateImageView(APIView):
    """
    API view to generate images using OpenAI.
    """

    def post(self, request):
        """
        Handle POST request to generate images.

        Returns:
            Response: Response with generated image data if successful.
        """
        data = request.data
        client = OpenAI(api_key=OPENAI_API_KEY)

        response = client.images.generate(
            model="dall-e-2",
            prompt=data,
            size="1024x1024",
            quality="standard",
            n=1,
        )
        output = response.data[0].url
        return Response({"data": output}, status=status.HTTP_200_OK)


class ProfileImageView(APIView):
    """
    API view to handle updating profile image.
    """

    def patch(self, request):
        """
        Handle PATCH request to update profile image.

        Returns:
            Response: Response indicating success or failure with appropriate
            status code and message.
        """
        try:
            image_data = request.data.get('image')
        except KeyError:
            return Response({'error': 'no update'}, status=status.HTTP_400_BAD_REQUEST)

        if image_data is None:
            return Response({'error': 'image empty'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            image_serializer = ProfileImageSerializer(data=request.data)
        except ValueError:
            return Response({'error': 'Given wrong data'}, status=status.HTTP_400_BAD_REQUEST)

        if not image_serializer.is_valid():
            return Response({'error': image_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user_data = User.objects.get(
                email=request.data.get('email'))
        except User.DoesNotExist:
            return Response({'error': 'Something went wrong'}, status=status.HTTP_400_BAD_REQUEST)

        user_data.image = image_serializer.validated_data.get('image')
        user_data.save()

        return Response({'updated_image': user_data.image.url}, status=status.HTTP_200_OK)
