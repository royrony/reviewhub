from __future__ import unicode_literals
from django.db import models
from django.utils import timezone
import datetime
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from taggit.managers import TaggableManager
from django.conf import settings
from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.contenttypes.fields import GenericRelation
from star_ratings.models import Rating

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    
    class Meta:
        ordering = ('name',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'
    
    def get_absolute_url(self):
        return reverse('list_of_post_by_category', args=[self.slug])
    
    def __str__(self):
        return self.name
    
class Post(models.Model):
    user=models.ForeignKey(User,blank=True,null=True)
    title=models.CharField(max_length=50)
    content=RichTextUploadingField()
    pic=models.ImageField(upload_to='pic',null=True,blank=True)
    ratings = GenericRelation(Rating, related_query_name='posts')
    category = models.ForeignKey(Category, blank=True)
    tags = TaggableManager(blank=True)
    date_created=models.DateTimeField(default=timezone.now,null=True,blank=True)
    moderated = models.BooleanField(default=False)
    def __unicode__(self):
        return self.title
    @property
    def total_likes(self):
        return self.likes.count()

class Profile(models.Model):
    user=models.OneToOneField(User)
    location=models.CharField(max_length=50,null=True,blank=True)
    gender_choices= (('M', 'Male'), ('F', 'Female'))
    gender = models.CharField(max_length=1, choices=gender_choices)
    profilepic=models.FileField(upload_to='pic',null=True,blank=True,default='pic/def.png')
    bio=models.CharField(max_length=100,null=True,blank=True)
    facebook=models.URLField(null=True,blank=True)
    twitter=models.URLField(null=True,blank=True)
    instagram=models.URLField(null=True,blank=True)
    
    class Meta:
        db_table='auth_profile'

    def __unicode__(self):
        return self.location

def create_user_profile(sender,instance,created,**kwargs):
    if created:
        Profile.objects.create(user=instance)

def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

post_save.connect(create_user_profile,sender=User)
post_save.connect(save_user_profile,sender=User)

class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments')
    name = models.CharField(max_length=80)
    #email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return 'Comment by {} on {}'.format(self.name, self.post)
