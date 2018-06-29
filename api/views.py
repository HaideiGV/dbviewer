import json
import uuid

from django.core.cache import cache
from django.http import (
    HttpResponse,
    Http404,
    HttpResponseNotAllowed,
    HttpResponseRedirect,
    HttpResponseBadRequest,
    JsonResponse,
)

from api.helpers import DB_MAP_CONNECTOR


def index(request):
    return HttpResponse("Text")


def init_connection(request):
    if str(request.method).lower() != 'post':
        return HttpResponseNotAllowed(['post'])

    data = json.loads(request.body)

    adapter = data.get('db_adapter', None)
    if not adapter:
        return Http404("db_adapter should be provided.")

    conn = DB_MAP_CONNECTOR[adapter](**data)

    response = HttpResponse("Connection initialized.")
    if conn:
        user_cookie = uuid.uuid4().hex
        cache.set(user_cookie, data)

        response.set_cookie("auth", user_cookie)
        conn.close()

    return response


def list_tables(request):
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
