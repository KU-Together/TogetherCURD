from django.shortcuts import render

from django.http import JsonResponse
from rest_framework import viewsets
from .models import User

class UserViewset(viewsets.ModelViewSet):
    def retrieve(self, request, user_id):
        user = User.objects.get(id=user_id)
        return JsonResponse(user.getValues())
    
    def create(self, request, *args, **kwargs):
        user = User()
        user.setValues(request.data)
        user.save()
        return JsonResponse(user.getValues())