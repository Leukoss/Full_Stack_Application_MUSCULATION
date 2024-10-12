from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render, redirect
from django.views import View
from .forms import SignUpForm,ExerciseForm
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_backends
from django.views.generic import DetailView
from django.http import JsonResponse
from .models import Exercise,Performance
from django.shortcuts import render, redirect, get_object_or_404

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
            'Développé incliné',
            'Squat', 
            'Soulevé de terre',
            'Curl',
            'Curl marteau',
            'Leg curl',
            'Leg Extension',
            'Pompe',
            'Traction',
            'Développé militaire',
            'Elevation latérale'
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

class ExerciseView(View):
    template_name = 'exercise.html'

    def get(self, request):
        exercises = Exercise.objects.filter(user=request.user)
        form = ExerciseForm()  
        return render(request, self.template_name, {'user': request.user, 'exercises': exercises, 'form': form})

    def post(self, request):
        form = ExerciseForm(request.POST)  

        if form.is_valid():
            exercise = form.save(commit=False)  
            exercise.user = request.user  
            exercise.save()  # Sauvegardez l'exercice
            return redirect('exercise_view_name')
        # Si le formulaire n'est pas valide, affichez à nouveau la page avec les erreurs
        exercises = Exercise.objects.filter(user=request.user)
        return render(request, self.template_name, {'user': request.user, 'exercises': exercises, 'form': form})
    


@login_required
def get_exercise_detail(request, exercise_id):
    # recover the exercise
    exercise = get_object_or_404(Exercise, id=exercise_id, user=request.user)
    data = {
        'name': exercise.name,
        'illustration': exercise.illustration.url if exercise.illustration else None,
    }
    return JsonResponse(data)

# View that get all the performances of a user on a specific exercise
@login_required
def exercise_performance_view(request, exercise_id):

    # get the exercise
    exercise = get_object_or_404(Exercise, id=exercise_id, user=request.user)
    
    # get the performance linked to the exercise
    performances = Performance.objects.filter(exercise=exercise)

    # create a dict getting ll the performances
    performance_data = []
    for performance in performances:
        performance_data.append({
            'date': performance.date.strftime('%Y-%m-%d'),
            'weights': performance.weights,
            'repetitions': performance.repetitions
        })

    return JsonResponse({'performances': performance_data})


# Get the 5 last performances of the user on a exercise
@login_required
def get_last_performances(request, exercise_id):
    exercise = Exercise.objects.get(id=exercise_id)

    # last 5 performance of a specific exercise
    performances = Performance.objects.filter(exercise=exercise).order_by('-id')[:5]

    # get the maximum number of set for a given performance
    if performances:
        max_sets = max([len(p.repetitions) for p in performances])
    else:
        max_sets = 0  

    # create datas for the table
    performance_data = []
    for performance in performances:
        # get the data to plot to the table
        row = {
            'date': performance.date.strftime('%d/%m/%Y'),
            'weights': performance.weights + [None] * (max_sets - len(performance.weights)),  # Remplir avec None si manque des sets
            'repetitions': performance.repetitions
        }
        performance_data.append(row)

    return JsonResponse({
        'exercise': exercise.name,
        'max_sets': max_sets,
        'performances': performance_data
    })


def home(request):
    return render(request, 'home.html', {'user': request.user})