from django.shortcuts import render, redirect
from .models import Post
from .forms import RegistrationForm, UserUpdate
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView


def home_page(request):
    posts = {
        'posts': Post.objects.all()
    }
    return render(request, 'blog/home_page.html', posts)

def about(request):
    return render(request, 'blog/about.html')


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created successfully. Log in below.")
            return redirect('login')
    else:
        form = RegistrationForm()

    return render(request, 'blog/register.html', {'form': form})

@login_required
def user_profile(request):
    if request.method == 'POST':
        u_form = UserUpdate(request.POST, instance=request.user)
        if u_form.is_valid():
            u_form.save()
            messages.success(request, "Account successfully updated.")
            return redirect('profile')
    else:
        u_form = UserUpdate(instance=request.user)

    data = {
        'user_form': u_form,
    }

    return render(request, 'blog/profile.html', data)

class PostDetailView(DetailView):
    model = Post

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    template_name = 'blog/post_edit.html'
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False