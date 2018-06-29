import psycopg2

from api.constants import POSTGRES_ADAPTER


def connect_to_postgres(host, port, username, password, db_name, **kwargs):
    try:
        conn = psycopg2.connect(
            host=host, user=username, password=password, dbname=db_name, port=port
        )
    except Exception as e:
        print(str(e))

    return conn


DB_MAP_CONNECTOR = {
    POSTGRES_ADAPTER: connect_to_postgres
}
