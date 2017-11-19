"""blog_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth.views import login, logout
from blog.views import (PostListView, PostDetailView,
						PostCreateView,PostUpdateView, 
						PostDeleteView, Draft, add_comment,
						publish_post, approve_comment,
						delete_comment, register_page,
						)

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', PostListView.as_view(), name='post_list'),
    url(r'^(?P<pk>\d+)/$', PostDetailView.as_view(), name='post_detail'),
    url(r'^create/$', PostCreateView.as_view(), name='create'),
    url(r'^(?P<pk>\d+)/edit/$', PostUpdateView.as_view(), name='edit'),
    url(r'^(?P<pk>\d+)/delete/$', PostDeleteView.as_view(), name='delete'),
    url(r'^drafts/$', Draft.as_view(), name='draft'),
    url(r'^(?P<pk>\d+)/comment/$', add_comment, name='comment'),
    url(r'^comments/(?P<pk>\d+)/approve/$', approve_comment, name='approve_comment'),
    url(r'^comments/(?P<pk>\d+)/delete/$', delete_comment, name='delete_comment'),
    url(r'^(?P<pk>\d+)/publish/$', publish_post, name='publish'),
    url(r'^register/$',register_page, name='register'),
    url(r'^accounts/login/$', login, name='login'),
    url(r'^accounts/logout/$', logout, name='logout', kwargs={'next_page': '/'}),
]