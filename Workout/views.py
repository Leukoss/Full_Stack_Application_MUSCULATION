from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render, redirect
from django.views import View
from .forms import SignUpForm
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .models import Exercise
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_backends
from django.views.generic import DetailView


class SignUpView(View):
    form_class = SignUpForm
    template_name = 'signup.html'

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            
            user = form.save()

            # creation of exercises for a user
            self.create_default_exercises(user)

            login(request, user)


            # Redirect to a success page
            return redirect('user_profile')
        return  render(request, self.template_name, {'form': form})
    
    # fonction that associates a list of basic exercises to a user
    def create_default_exercises(self, user):
        # Set of default exercises for all users
        default_exercises = [
            'Développé couché', 
            'Squat', 
            'Soulevé de terre',
            'Curl',
            'Curl marteau'
            'Leg curl',
            'Leg Extension'
        ]
        for exercise_name in default_exercises:
            Exercise.objects.create(name=exercise_name, user=user)

class CustomLoginView(LoginView):
    # Page to log in
    template_name = 'registration/login.html'

    # Redirect to the profil page after a successful login
    def get_success_url(self):
        # go to the profile page
        return self.get_redirect_url() or reverse('user_profile')

# View of the page of the user
@method_decorator(login_required, name='dispatch')
class UserProfileView(View):
    template_name = 'user_profile.html'


    def get(self, request):

        exercises = Exercise.objects.filter(user=request.user)

        # display the page of the connected user
        return render(request, self.template_name, {'user': request.user, 'exercises': exercises})

class ExerciseDetailView(DetailView):
    model = Exercise
    template_name = 'exercise_detail.html'


def home(request):
    return render(request, 'home.html', {'user': request.user})