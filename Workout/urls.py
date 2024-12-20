from django.urls import path
from . import views
from .views import SignUpView, LoginView, LogoutView, UserProfileView,ExerciseView,ExerciseDetailView
urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('exercise/',ExerciseView.as_view(), name="exercise"),
    path('profile/', UserProfileView.as_view(), name='user_profile'),
    path('exercise/<int:exercise_id>/detail/', ExerciseDetailView.as_view(), name='exercise_detail'),
    path('exercise/<int:exercise_id>/get_last_performances', views.get_last_performances,name = 'exercise_last_performance'),
    path('exercise/<int:exercise_id>/performances/', views.exercise_performance_view, name='exercise_performance'),
    path('exercise/', ExerciseView.as_view(), name='exercise_view_name')
]
