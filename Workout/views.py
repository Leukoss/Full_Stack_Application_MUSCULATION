from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render, redirect
from django.views import View
from .forms import SignUpForm,ExerciseForm,PerformanceForm
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_backends
from django.views.generic import DetailView
from django.http import JsonResponse
from .models import Exercise,Performance
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

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

from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Exercise, Performance
from .forms import PerformanceForm, ExerciseForm

class ExerciseView(View):
    template_name = 'exercise.html'

    def get(self, request):
        exercises = Exercise.objects.filter(user=request.user)
        exercise_form = ExerciseForm()  # Formulaire pour ajouter un exercice
        performance_form = PerformanceForm()  # Formulaire pour ajouter une performance
        return render(request, self.template_name, {
            'user': request.user,
            'exercises': exercises,
            'exercise_form': exercise_form,
            'performance_form': performance_form,
        })

    def post(self, request):
        exercises = Exercise.objects.filter(user=request.user)
        exercise_form = ExerciseForm()
        performance_form = PerformanceForm()

        # Handle Exercise Submission
        if 'exercise' in request.POST:
            exercise_form = ExerciseForm(request.POST)
            if exercise_form.is_valid():
                exercise = exercise_form.save(commit=False)
                exercise.user = request.user
                exercise.save()
                return redirect('exercise_view_name')

        # Handle Performance Submission
        if 'performance' in request.POST:
            # Imprimer les données POST pour le débogage
            print("Données reçues de POST :", request.POST)

            performance_form = PerformanceForm(request.POST)
            if performance_form.is_valid():

                exercise_id = request.POST.get('exercise_id')
                if exercise_id:

                    try:
                        exercise = Exercise.objects.get(id=exercise_id)

                        # Récupérer les poids et répétitions
                        weights_str = request.POST.getlist('weights')
                        repetitions_str = request.POST.getlist('repetitions')

                        print("Voici les poids en str :" + " ".join(str(e) for e in weights_str))
                        print("Voici les poids en str :" + " ".join(str(e) for e in repetitions_str))

                        # Vérifier les champs vides
                        if not weights_str or not repetitions_str:
                            messages.error(request, "Les poids et les répétitions ne peuvent pas être vides.")
                            return render(request, self.template_name, {'user': request.user, 'exercises': exercises, 'exercise_form': exercise_form, 'performance_form': performance_form})

                        # Convertir les chaînes en listes de nombres
                        weights = [float(weight.strip()) for weight in weights_str if weight.strip()]
                        print("Poids" + " ".join(str(e) for e in weights))
                        repetitions = [int(repetition.strip()) for repetition in repetitions_str if repetition.strip()]
                        print("Repetitions " + " ".join(str(e) for e in repetitions))
                        
                        # Vérifier si les longueurs correspondent
                        if len(weights) != len(repetitions):
                            messages.error(request, "Le nombre de poids et de répétitions doit être identique.")
                        else:
                            performance = performance_form.save(commit=False)
                            performance.exercise = exercise
                            performance.weights = weights  # Enregistrer en tant que JSON
                            performance.repetitions = repetitions  # Enregistrer en tant que JSON
                            performance.save()

                            # Imprimer les données de performance dans le terminal
                            print(f'Performance enregistrée : Exercice: {exercise.name}, Date: {performance.date}, Poids: {weights}, Répétitions: {repetitions}')

                            messages.success(request, "Performance ajoutée avec succès.")
                            return redirect('exercise_view_name')

                    except Exercise.DoesNotExist:
                        messages.error(request, "L'exercice sélectionné n'existe pas.")
                else:
                    messages.error(request, "ID de l'exercice manquant.")

            else:
                print("Le formulaire de performance n'est pas valide")
                print(performance_form.errors)  # Afficher les erreurs de validation
                messages.error(request, "Le formulaire de performance contient des erreurs.")

        # Rendre le template avec les performances
        return render(request, self.template_name, {
            'user': request.user,
            'exercises': exercises,
            'exercise_form': exercise_form,
            'performance_form': performance_form,
        })


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