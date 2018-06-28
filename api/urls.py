from django.urls import path

from .views import index, init_connection

urlpatterns = [
    path('', index, name='index'),
    path('init', init_connection, name='init_connection'),
]
