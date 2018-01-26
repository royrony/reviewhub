from django.contrib import admin
from .models import *
from django.contrib.auth.models import User
# Register your models here.
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'post', 'created', 'active')
    list_filter = ('active', 'created', 'updated')
    search_fields = ('name', 'body')
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'content', 'date_created', 'moderated')
    list_filter = ('moderated', 'date_created')
    search_fields = ('title', 'content')
admin.site.register(Comment, CommentAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Profile)
admin.site.register(Category)

