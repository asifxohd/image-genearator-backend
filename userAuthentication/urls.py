from django.urls import path
from .views import RegisterView, RetriveUserView, GenrateImageView, ProfileImageView, UpdateUserProfileInfoView ,ListUsersViewAdmin,DeleteUserView,UpdateUserProfileAdmin, SearchQuery


urlpatterns = [
    path("register/", RegisterView.as_view()),
    path("userinfo/", RetriveUserView.as_view()),
    path('img/', GenrateImageView.as_view()), 
    path('edit-profile-image/', ProfileImageView.as_view()),
    path('update-user-info/',UpdateUserProfileInfoView.as_view()),
    path('list-users/', ListUsersViewAdmin.as_view()),
    path('delete-user/<str:id>/', DeleteUserView.as_view()),
    path('update-user-admin/<str:id>/', UpdateUserProfileAdmin.as_view()),
    path('search/',SearchQuery.as_view()),

]
