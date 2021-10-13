from psycopg2.extras import RealDictCursor

import connection


@connection.connection_handler
def get_all_content(cursor: RealDictCursor):
    query = """
        SELECT *
        FROM content
        ORDER BY title"""
    cursor.execute(query)
    return cursor.fetchall()


@connection.connection_handler
def get_all_users(cursor: RealDictCursor):
    query = """
        SELECT *
        FROM admin_user"""
    cursor.execute(query)
    return cursor.fetchall()


@connection.connection_handler
def get_company_info(cursor: RealDictCursor):
    query = """
        SELECT *
        FROM company_info"""
    cursor.execute(query)
    return cursor.fetchall()


def get_public_categories():
    all_content = get_all_content()

    categories = []

    for category in all_content:
        if category['public'] and category['category'] not in categories:
            categories.append(category['category'])

    categories.sort()
    return categories


def get_all_categories():
    all_content = get_all_content()

    categories = []

    for category in all_content:
        categories.append(category['category'])

    return categories


def get_public_content_by_category(category):
    all_content = get_all_content()
    filtered_content = []

    for content in all_content:
        if content['category'] == category and content['public'] is True:
            filtered_content.append(content)

    return filtered_content
