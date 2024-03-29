from django.contrib.auth.models import User
from django.views.generic.edit import CreateView
from .forms import SignUpForm


class SignUpView(CreateView):
    model = User
    form_class = SignUpForm
    success_url = '/'
    template_name = 'registration/signup.html'
