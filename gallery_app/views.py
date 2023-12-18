from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.views.generic import ListView
from .models import *
from django.shortcuts import redirect, render


class PostListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'gallery_app/index.html'
    context_object_name = 'posts'
    login_url = 'login'

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['username'] = self.request.user.username
        return context
    
    
class RegisterView(View):
    template_name = 'registration/register.html'
    form_class = UserCreationForm

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')  # Змініть 'home' на URL вашої головної сторінки
        return render(request, self.template_name, {'form': form})