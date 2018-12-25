from django.contrib.auth import authenticate, login
from django.db import transaction
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView

from users.forms import SignUpForm
from users.models import User


class SignupView(CreateView):
    model = User
    form_class = SignUpForm
    template_name = 'registration/signup.html'

    @transaction.atomic()
    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return HttpResponseRedirect(reverse_lazy('categories'))
        return render(request, 'registration/signup.html', {'form': form})
