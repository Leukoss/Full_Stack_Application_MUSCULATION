import pycountry
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from pycountry import countries
from .models import Exercise, UserProfile,Performance

class SignUpForm(UserCreationForm):
    username = forms.CharField(
        required=True,
        max_length=25,
        widget=forms.TextInput(attrs={'placeholder': 'Nom d\'utilisateur'})
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'placeholder': 'Adresse électronique'})
    )
    password1 = forms.CharField(
        required=True,
        max_length=25,
        widget=forms.PasswordInput(attrs={'placeholder': 'Mot de passe'})
    )
    password2 = forms.CharField(
        required=True,
        max_length=25,
        widget=forms.PasswordInput(
            attrs={'placeholder': 'Confirmer le mot de passe'})
    )
    age = forms.IntegerField(
        required=True,
        widget=forms.NumberInput(attrs={'placeholder': 'Âge',
                                        'class': 'no-spinner'})
    )
    weight = forms.DecimalField(
        required=True,
        widget=forms.NumberInput(attrs={'placeholder': 'Poids (kg)',
                                        'class': 'no-spinner'})
    )
    height = forms.DecimalField(
        required=True,
        widget=forms.NumberInput(attrs={'placeholder': 'Taille (cm)',
                                        'class': 'no-spinner'})
    )
    activity = forms.ChoiceField(
        required=True,
        choices=[(1.2, 'Sédentaire'), (1.375, 'Légèrement Actif'),
                 (1.55, 'Actif'), (1.725, 'Très Actif'),
                 (1.9, 'Extrêmement acitf')],
        widget=forms.Select(attrs={'placeholder': 'Niveau d\'activité'})
    )
    country = forms.ChoiceField(
        required=True,
        widget=forms.Select(attrs={'placeholder': 'Pays de résidence'})
    )

    class Meta:
        model = User
        fields = (
        'username', 'email', 'password1', 'password2', 'age', 'weight',
        'height', 'activity', 'country')

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        self.fields['country'].choices = [(country.alpha_2, country.name) for
                                          country in pycountry.countries]

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']

        if commit:
            user.save()

            # Save profile with the additional fields
            profile = UserProfile.objects.create(
                user=user,
                age=self.cleaned_data.get('age'),
                weight=self.cleaned_data.get('weight'),
                height=self.cleaned_data.get('height'),
                activity=self.cleaned_data.get('activity'),
                country=self.cleaned_data.get('country')
            )

            # Calculate IMC (BMI) using weight (kg) and height (cm)
            weight = self.cleaned_data.get('weight')
            height_in_meters = self.cleaned_data.get(
                'height') / 100  # convert cm to meters
            if height_in_meters > 0:
                profile.imc = weight / (height_in_meters ** 2)
            else:
                profile.imc = None  # Fallback to None if height is zero or invalid

            profile.save()
        return user


class ExerciseForm(forms.ModelForm):

    # Champs pour le nom de l'exercice
    name = forms.CharField(
        required=True,
        max_length=100,
        widget=forms.TextInput(attrs={
            'placeholder': 'Nom de l\'exercice',
            'class': 'form-control'
        })
    )

    class Meta:
        model = Exercise
        exclude = ["user","exercise_id"]

    def __init__(self, *args, **kwargs):
        super(ExerciseForm, self).__init__(*args, **kwargs)

class PerformanceForm(forms.ModelForm):
    
    repetitions = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'ex: 12, 10, 8'})
    )
    weights = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'ex: 50, 45, 40'})
    )

    class Meta:
        model = Performance
        fields = ['repetitions', 'weights']
