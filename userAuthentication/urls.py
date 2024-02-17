from django.urls import path
from .views import RegisterView, RetriveUserView, GenrateImageView, ProfileImageView


urlpatterns = [
    path("register/", RegisterView.as_view()),
    path("userinfo/", RetriveUserView.as_view()),
    path('img/', GenrateImageView.as_view()), 
    path('edit-profile-image/', ProfileImageView.as_view()),

]
