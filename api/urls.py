from django.urls import path

from .views import (
    index,
    init_connection,
    get_db_tables_list,
    get_db_table_rows,
)

urlpatterns = [
    path('', index, name='index'),
    path('init', init_connection, name='init_connection'),
    path('tables', get_db_tables_list, name='get_db_tables_list'),
    path('tables/<slug:table_name>/rows', get_db_table_rows, name='get_db_table_rows'),
]
