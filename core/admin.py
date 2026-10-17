from django.contrib import admin # type: ignore
from core.models import Profile, Post, Comment # type: ignore

# Registers models to make them accessible inside http://127.0.0
admin.site.register(Profile)
admin.site.register(Post)
admin.site.register(Comment)
