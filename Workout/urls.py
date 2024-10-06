from django.urls import path
from . import views
from .views import SignUpView, LoginView, LogoutView, UserProfileView

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', UserProfileView.as_view(), name='user_profile'),
    path('exercise/<int:exercise_id>/', views.get_exercise_detail,name = "exercise_detail")
]
