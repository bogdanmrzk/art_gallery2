from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views import View
from .forms import *
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import *
from django.shortcuts import redirect, render, get_object_or_404


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
    
    
class PostDetailView(DetailView):
    model = Post
    template_name = 'gallery_app/post_detail.html'
    context_object_name = 'post'


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'gallery_app/post_form.html'
    success_url = reverse_lazy('posts')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'gallery_app/post_form.html'
    context_object_name = 'post'
    success_url = reverse_lazy('posts')


class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'registration/post_confirm_delete.html'
    success_url = reverse_lazy('posts')

    
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
            return redirect('posts')  # Redirect to main page
        return render(request, self.template_name, {'form': form})
    
    
class CustomLoginView(LoginView):
    form_class = LoginForm
    template_name = 'registration/login.html'


class LogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect(reverse_lazy('register'))
        

class LikePostView(View):
    def post(self, request, post_id):
        post = get_object_or_404(Post, pk=post_id)
        user = request.user

        if Like.objects.filter(user=user, post=post).exists():
            return JsonResponse({'error': 'Ви вже залишили лайк для цього поста'}, status=400)
        else:
            Like.objects.create(user=user, post=post)
            post.likes += 1
            post.save()

        likes_count = post.like_set.count()
        return JsonResponse({'likes_count': likes_count})
