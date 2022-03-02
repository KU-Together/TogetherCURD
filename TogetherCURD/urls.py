"""TogetherCURD URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path

from kanban.views import UserViewset, CardViewset

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/<int:user_id>', UserViewset.as_view({'get':'retrieve'})),
    path('user', UserViewset.as_view({'post':'create'})),
    path('user/<int:user_id>/board/<int:board_id>/status/<status>/card', CardViewset.as_view({'get':'list', 'post':'create'})),
    path('user/<int:user_id>/board/<int:board_id>/status/<status>/card/<int:card_id>', CardViewset.as_view({'patch':'partial_update', 'delete': 'destroy'})),
]