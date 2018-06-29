import json
import uuid

from django.core.cache import cache
from django.http import (
    HttpResponse,
    Http404,
    HttpResponseBadRequest,
    JsonResponse,
    HttpResponseRedirect,
)

from api.helpers import DB_MAP_CONNECTOR
from api.constants import DB_QUERY_LIMIT


def index(request):
    return HttpResponse("Text")


def init_connection(request):
    data = json.loads(request.body)

    adapter = data.pop('db_adapter', None)
    if not adapter:
        return Http404("db_adapter should be provided.")

    is_connected = DB_MAP_CONNECTOR[adapter](**data)

    response = HttpResponse("Connection initialized.")
    if is_connected:
        user_cookie = uuid.uuid4().hex
        cache.set(user_cookie, data)

        response.set_cookie("auth", user_cookie)

    return response


def get_db_tables_list(request):
    cookie = request.COOKIES.get('auth')

    if not cookie:
        return HttpResponseRedirect(redirect_to='/')

    conn_params = cache.get(cookie)

    if not conn_params:
        return HttpResponseBadRequest("Session was expired. Try to reconnect.")

    conn = DB_MAP_CONNECTOR[conn_params['db_adapter']](**conn_params)

    cursor = conn.cursor()
    cursor.execute(
        "SELECT table_name FROM information_schema.tables "
        "WHERE table_schema = 'public' "
        "ORDER BY table_schema,table_name;"
    )

    return JsonResponse([row[0] for row in cursor.fetchall()], safe=False)


def get_db_table_rows(request, table_name):
    cookie = request.COOKIES.get('auth')

    if not cookie:
        return HttpResponseRedirect(redirect_to='/')

    conn_params = cache.get(cookie)

    if not conn_params:
        return HttpResponseBadRequest("Session was expired. Try to reconnect.")

    conn = DB_MAP_CONNECTOR[conn_params['db_adapter']](**conn_params)

    cursor = conn.cursor()

    cursor.execute(
        "SELECT table_name FROM information_schema.tables "
        "WHERE table_schema = 'public' AND table_name = '{}'".format(table_name)
    )

    if not cursor.fetchall():
        return HttpResponseBadRequest("Table doesn't exists.")

    cursor.execute(
        "SELECT column_name FROM information_schema.columns "
        "WHERE table_schema = 'public' "
        "AND table_name = '{table_name}'"
        .format(table_name=table_name)
    )

    columns = [c[0] for c in cursor.fetchall()]

    cursor.execute(
        "SELECT * FROM public.{table_name} LIMIT {limit};"
        .format(table_name=table_name, limit=DB_QUERY_LIMIT)
    )

    rows = cursor.fetchall()

    data = {}
    for i, row in enumerate(rows):
        data[i] = dict(zip(columns, row))

    return JsonResponse(data, safe=False)
