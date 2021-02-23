from django.urls import path, re_path

from Accounts.views import Login, Logout, RegisterView, ProfileView, add_address, EditProfileView

urlpatterns = [
    path('login/', Login.as_view(), name='login'),
    path('logout/', Logout.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('add_address/', add_address, name='add_address'),
    path('edit_profile/', EditProfileView.as_view(), name='edit_profile'),
]
