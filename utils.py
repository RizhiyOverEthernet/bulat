import psycopg2


def database(sql):
    """
    Функция выбора записей из конкретной базы данных
    """

    database_setting = psycopg2.connect(user="*",
                                        password="*",
                                        host="/var/run/postgresql",
                                        port=5432,
                                        database="*")

    with database_setting as connection:
        with connection.cursor() as cursor:
            cursor.execute(sql)
            return cursor.fetchone()
