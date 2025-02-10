from django.urls import path, include
from django.contrib.auth import views as auth_views
from users.forms import CustomAuthenticationForm

urlpatterns = [
   
    path('accounts/login/', auth_views.LoginView.as_view(authentication_form=CustomAuthenticationForm), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
]