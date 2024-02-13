from rest_framework.views import APIView
from rest_framework import permissions, status
from rest_framework.response import Response
from .serializers import UserAccountModelSerializer, UserSerializer


class RegisterView(APIView):
    def post(self, request):
        serializer = UserAccountModelSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        user = serializer.create(serializer.validated_data)
        user = UserSerializer(user)

        return Response(user.data, status=status.HTTP_201_CREATED)


class RetriveUserView(APIView):
    permissions_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = UserSerializer(request.user)
        return Response(user.data, status=status.HTTP_200_OK)
