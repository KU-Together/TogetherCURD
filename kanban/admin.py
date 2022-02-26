from django.contrib import admin
from .models import User, Board, List, Card

admin.site.register(User)
admin.site.register(Board)
admin.site.register(List)
admin.site.register(Card)