from difflib import context_diff
from msilib.schema import ListView
from operator import truediv
from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse
from .models import Post
from django.views.generic import (ListView, DetailView,CreateView,UpdateView,DeleteView)
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.contrib.auth.models import User
# Create your views here.



def home(request):
    context = {
        'test1' : Post.objects.all(),
        'title' : 'TITLE'
    }

    return render (request, 'blog/home.html', context)


class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'test1'
    ordering = ['-date_posted']
    paginate_by = 5


class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html'
    context_object_name = 'test2'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User,username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')



class PostDetailView(DetailView):
    model = Post   #here we are not giving any context_object_name to write in the corresponding html page so you use keyword "object" in the html page.


class PostCreateView(LoginRequiredMixin,CreateView):
    # The CreateView page displayed to a GET request uses a template_name_suffix of '_form'
    model = Post
    fields = ['title', 'content']

    def form_valid(self,form):   # when used this function it fills the author instance of the form and retunrs the valid data and django saves it
                                # we should only use form_valid as the name of the function 
        form.instance.author = self.request.user
        return super().form_valid(form)
    

class PostUpdateView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self,form):
        form.instance.author = self.request.user
        return super().form_valid(form)


    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    model = Post
    success_url='/blog'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False
    



def about(request):
    return render(request, 'blog/about.html', {'title' : 'ABOUT'})



 