import json
import uuid

from django.core.cache import cache
from django.http import HttpResponse, Http404

from api.helpers import DB_MAP_CONNECTOR


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
