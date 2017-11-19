from django.db import models
from django.utils import timezone
from django.core.urlresolvers import reverse
# Create your models here.

class Post(models.Model):
	author = models.ForeignKey('auth.User')
	title = models.CharField(max_length=120)
	text  = models.TextField()
	created_date = models.DateTimeField(auto_now_add=True)
	published_date = models.DateTimeField(blank=True, null=True)

	def publish(self):
		self.published_date = timezone.now()
		self.save()

	def approved_comments(self):
		self.comments.filter(approve_comment=True)

	def get_absolute_url(self):
		return reverse('post_detail', kwargs={'pk':self.pk})

	def __str__(self):
		return self.title

	class Meta:
		ordering = ['-published_date']

class Comment(models.Model):
	post = models.ForeignKey('Post', related_name='comments')
	author =  models.CharField(max_length=120)
	text = models.TextField()
	timestamp = models.DateTimeField(auto_now_add=True)
	approve_comment = models.BooleanField(default=False)

	def approve(self):
		self.approve_comment = True
		self.save()

	# def get_absolute_url(self):
	# 	return reverse('post_detail')

	def __str__(self):
		return self.text