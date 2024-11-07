from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.views.generic import TemplateView

# Create your views here.


class HomeView(TemplateView):
    template_name = 'users/home.html'


def log_out_view(request):
    logout(request)
    return redirect('home')
