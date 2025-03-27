from django.contrib import admin
from .models import Post, Comment

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'author', 'created_at')
    list_filter = ('author', 'created_at')
    search_fields = ('title', 'content', 'author__username')
    ordering = ('-created_at',)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'post', 'author', 'created_at')
    list_filter = ('author', 'created_at')
    search_fields = ('content', 'author__username')
    ordering = ('-created_at',)
