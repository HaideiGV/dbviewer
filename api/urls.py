from django.urls import path

from .views import index, init_connection, list_tables

urlpatterns = [
    path('', index, name='index'),
    path('init', init_connection, name='init_connection'),
    path('show-tables', list_tables, name='list_tables'),
]
