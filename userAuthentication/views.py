"""  imports  """

from rest_framework import permissions, status
from rest_framework. permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from openai import OpenAI
from django.db.models import Q
from magic_words.settings import OPENAI_API_KEY
from django.contrib.auth import get_user_model
from .models import UserAccount
from .utils import CustomTokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import (
    UserAccountModelSerializer,
    UserSerializer,
    ProfileImageSerializer,
    PasswordSerializers

)
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
            return Response(
                {"validation_errors": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )

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
            image_data = request.data.get("image")
        except KeyError:
            return Response({"error": "no update"}, status=status.HTTP_400_BAD_REQUEST)

        if image_data is None:
            return Response(
                {"error": "image empty"}, status=status.HTTP_400_BAD_REQUEST
            )

        try:
            image_serializer = ProfileImageSerializer(data=request.data)
        except ValueError:
            return Response(
                {"error": "Given wrong data"}, status=status.HTTP_400_BAD_REQUEST
            )

        if not image_serializer.is_valid():
            return Response(
                {"error": image_serializer.errors}, status=status.HTTP_400_BAD_REQUEST
            )

        try:
            user_data = User.objects.get(email=request.data.get("email"))
        except User.DoesNotExist:
            return Response(
                {"error": "Something went wrong"}, status=status.HTTP_400_BAD_REQUEST
            )

        user_data.image = image_serializer.validated_data.get("image")
        user_data.save()

        return Response(
            {"updated_image": user_data.image.url}, status=status.HTTP_200_OK
        )


class CustomTokenObtainPairView(TokenObtainPairView):
    """
    Custom view for obtaining token pairs with extended payload data.

    This view extends TokenObtainPairView to provide customized token pairs
    with additional payload data, such as username and phone number.
    It uses CustomTokenObtainPairSerializer to generate tokens.

    Attributes:
        serializer_class (CustomTokenObtainPairSerializer): The serializer class
            used to obtain token pairs with extended payload data.
    """

    serializer_class = CustomTokenObtainPairSerializer


class UpdateUserProfileInfoView(APIView):
    """
    API view to update user profile information.
    """

    def put(self, request):
        """
        Handle PUT request to update user profile.

        Args:
            request: The HTTP request object.

        Returns:
            Response: JSON response with updated user profile data or error messages.
        """
        user_obj = UserAccount.objects.get(email=request.user.email)
        serializer = PasswordSerializers(user_obj, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ListUsersViewAdmin(APIView):
    """
    API endpoint to list all non-superuser accounts for admin users.
    Only accessible to superusers.

    HTTP Methods:
        - POST: Retrieves and returns a list of non-superuser accounts.

    Permission Classes:
        - IsAdminUser: Only admin users are allowed to access this endpoint.
    """

    permission_classes = [IsAdminUser]

    def post(self, request):
        """
        POST method handler.

        Retrieves and returns a list of non-superuser accounts.
        Returns a 401 Unauthorized response if the user is not a superuser.

        Parameters:
            request (Request): The HTTP request object.

        Returns:
            Response: A Response object containing a list of non-superuser accounts
                      serialized as JSON, or a 401 Unauthorized response.
        """
        if request.user.is_superuser:
            user_data = UserAccount.objects.exclude(is_superuser=True).values(
                'id', 'username', 'email', 'phone_number', 'password'
            )
            user_serializer = UserSerializer(user_data, many=True)

            return Response(user_serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(
                {'error': 'Unauthorized access. Only superusers can perform this action.'},
                status=status.HTTP_401_UNAUTHORIZED
            )


class DeleteUserView(APIView):
    """
    DeleteUserView:
    ---
    This API endpoint allows deleting a user account.

    Parameters:
    - id: The ID of the user to be deleted.

    Returns:
    - Success message if the user is deleted successfully.
    - Error message if the user is not found.
    """

    def delete(self, request, id):
        """
        Delete a user with the specified ID.

        Args:
            request: The HTTP request object.
            id (int): The ID of the user to delete.

        Returns:
            Response: A response indicating the outcome of the deletion operation.
                - If the user is found and successfully deleted, returns a 204 No Content response.
                - If the user is not found, returns a 404 Not Found response.
        """
        try:
            user = UserAccount.objects.get(id=id)
            user.delete()
            return Response({'message': 'User deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
        except UserAccount.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)


class UpdateUserProfileAdmin(APIView):
    """
    UpdateUserProfileAdmin:
    ---
    This API endpoint allows updating user profile information.

    Parameters:
    - id: The ID of the user whose profile needs to be updated.

    Request Body:
    - username: The new username for the user.
    - email: The new email for the user.
    - phone_number: The new phone number for the user.

    Returns:
    - Updated user profile data if successful.
    - Error message if the user profile is not found or if there are validation errors in the input data.
    """

    def put(self, request, id):
        """
        Update a user profile with the specified ID.

        Args:
            request: The HTTP request object containing the updated user data.
            id (int): The ID of the user profile to update.

        Returns:
            Response: A response indicating the outcome of the update operation.
                - If the user profile is found, updated successfully, and the data is valid,
                returns a 200 OK response along with the updated user data.
                - If the user profile is not found, returns a 404 Not Found response.
                - If the provided data is invalid, returns a 400 Bad Request response along
                with the validation errors.
        """
        try:
            user = UserAccount.objects.get(pk=id)
        except UserAccount.DoesNotExist:
            return Response({"error": "User profile not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = UserAccountModelSerializer(user, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SearchQuery(APIView):
    """
    API endpoint for searching users based on a query.
    """

    def post(self, request):
        """
        Handle POST request for searching users based on a query.
        """
        search = (request.data.get('search')).strip()
        try:
            if search != '':
                users_data = User.objects.filter(Q(username__icontains=search) | Q(email__icontains=search) | Q(phone_number__icontains=search)).exclude(is_superuser=True).all().order_by('username')
            else:
                users_data = User.objects.all().exclude(is_superuser=True).order_by('id')
            serialize = UserSerializer(users_data, many=True)
            return Response(serialize.data, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"error": "Something went wrong"}, status=status.HTTP_400_BAD_REQUEST)