from rest_framework.views import APIView
from rest_framework import permissions, status
from rest_framework.response import Response
from .serializers import UserAccountModelSerializer, UserSerializer
from openai import OpenAI
from magic_words.settings import OPENAI_API_KEY

class RegisterView(APIView):
    def post(self, request):
        serializer = UserAccountModelSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({'validation_errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        user = serializer.create(serializer.validated_data)
        user = UserSerializer(user)

        return Response(user.data, status=status.HTTP_201_CREATED)


class RetriveUserView(APIView):
    permissions_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = UserSerializer(request.user)
        return Response(user.data, status=status.HTTP_200_OK)



class GenrateImageView(APIView):
    def post(self, request):
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
        return Response({"data":output},status=status.HTTP_200_OK)
