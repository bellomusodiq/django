from django.shortcuts import render, get_object_or_404, redirect, render_to_response
from django.http import HttpResponseRedirect
from .models import Post, Comment
from .forms import PostForm, CommentForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.views.generic import (	ListView, DetailView,
									CreateView, UpdateView,
									DeleteView, FormView,
									)
# Create your views here.
class PostListView(ListView):
	model = Post
	def get_queryset(self):
		return Post.objects.filter(published_date__lte=timezone.now())

class Draft(ListView):
	model = Post
	template_name = 'blog/draft.html'
	def get_queryset(self):
		return Post.objects.filter(published_date__isnull=True)

class PostDetailView(DetailView):
	model = Post
	def get_context_data(self, **kwargs):
	    context = super().get_context_data(**kwargs)
	    context['form1'] = CommentForm
	    return context

class PostCreateView(LoginRequiredMixin, CreateView):
	model = Post
	redirect_field_name = 'blog/post_detail.html'
	login_url = '/login/'
	form_class = PostForm

	def form_valid(self, form):
	    form.instance.author = self.request.user
	    return super(PostCreateView, self).form_valid(form)

class PostUpdateView(LoginRequiredMixin, UpdateView):
	model = Post
	redirect_field_name = 'blog/post_detail.html'
	login_url = '/login/'
	form_class = PostForm

class PostDeleteView(LoginRequiredMixin, DeleteView):
	model = Post
	success_url = reverse_lazy('post_list')

from django.contrib import messages
def add_comment(request, pk):
	post = get_object_or_404(Post, pk=pk)
	if request.method == 'POST':
		form1 = CommentForm(request.POST)
		if form1.is_valid():
			comment = form1.save(commit=False)
			comment.post = post
			comment.save()
			messages.success(request, 'Your comment will be reviewed by the admin')
			return redirect('post_detail', pk=post.pk)
	else:
		form1 = CommentForm()
	return render(request, 'blog/comment.html', {'form1':form1})

@login_required
def approve_comment(request, pk):
	comment = get_object_or_404(Comment, pk=pk)
	comment.approve()
	return redirect('post_detail', pk=comment.post.pk)

@login_required
def delete_comment(request, pk):
	comment = get_object_or_404(Comment, pk=pk)
	post_pk = comment.post.pk
	comment.delete()
	return redirect('post_detail', pk=post_pk)

@login_required
def publish_post(request, pk):
	post = get_object_or_404(Post, pk=pk)
	post.publish()
	return redirect('post_detail', pk=post.pk)

from django.template import RequestContext
from .forms import RegistrationForm
from django.http import Http404
from django.contrib.auth.models import User
def register_page(request):
	if not request.user.is_authenticated:
	    if request.method == 'POST':
	        form = RegistrationForm(request.POST)
	        if form.is_valid():
	            user = User.objects.create_user(username=form.cleaned_data['username'],password=form.cleaned_data['password1'],email=form.cleaned_data['email'])
	            return HttpResponseRedirect('/')
	    form = RegistrationForm()
	    variables = {'form': form}
	else:
		return HttpResponseRedirect("/")
	return render(request, 'registration/register.html',variables)