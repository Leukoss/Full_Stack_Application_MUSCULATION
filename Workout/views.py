from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render, redirect
from django.views import View
from .forms import SignUpForm


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
            login(request, user)
            # Redirect to a success page
            return redirect('home')
        return render(request, self.template_name, {'form': form})

class CustomLoginView(LoginView):
    # Page to log in
    template_name = 'registration/login.html'

class CustomLogoutView(LogoutView):
    # Redirect to a success page after logout
    next_page = 'home'

def home(request):
    return render(request, 'home.html', {'user': request.user})