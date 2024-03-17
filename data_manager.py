from psycopg2.extras import RealDictCursor

import connection


@connection.connection_handler
def get_all_content_preview(cursor: RealDictCursor):
    query = """
        SELECT id, title, SUBSTRING(description from 0 for 200) as description, category, public
        FROM content
        ORDER BY category"""
    cursor.execute(query)
    return cursor.fetchall()


@connection.connection_handler
def get_all_content(cursor: RealDictCursor):
    query = """
        SELECT *
        FROM content
        ORDER BY last_modified ASC"""
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
        FROM company_info
        WHERE id = 1"""
    cursor.execute(query)
    return cursor.fetchall()[0]


def get_public_categories():
    all_content = get_all_content()

    categories = []

    for category in all_content:
        if category['public'] and category['category'] not in categories:
            categories.append(category['category'])

    return categories


def get_all_categories():
    all_content = get_all_content()

    categories = []

    for category in all_content:
        if category['category'] not in categories:
            categories.append(category['category'])

    return categories


def get_public_content_by_category(category):
    all_content = get_all_content()
    filtered_content = []

    for content in all_content:
        if content['category'] == category and content['public'] is True:
            filtered_content.append(content)

    return filtered_content


@connection.connection_handler
def update_admin(cursor: RealDictCursor, user_name, password):
    query = """UPDATE admin_user
               SET user_name = %s, password = %s
               WHERE id = 1"""
    values = (user_name, password)

    cursor.execute(query, values)


@connection.connection_handler
def get_admin(cursor: RealDictCursor):
    query = """
            SELECT *
            FROM admin_user
            WHERE id = 1"""
    cursor.execute(query)

    return cursor.fetchall()[0]


@connection.connection_handler
def save_content(cursor: RealDictCursor, data):
    query = """INSERT INTO content(id, title, description, image, image_direction, public, last_modified, category, image_source)
                VALUES (DEFAULT, %s, %s, %s, %s, %s, TIMESTAMP %s, %s, %s)
                """

    values = [data['title'],
              data['description'],
              data['image'],
              data['image_direction'],
              data['public'],
              data['last_modified'],
              data['category'],
              data['image_source']]

    cursor.execute(query, values)


@connection.connection_handler
def get_content(cursor: RealDictCursor, content_id: str):
    query = """SELECT * FROM content
    WHERE id = %s;"""
    print("content id:" + content_id)
    cursor.execute(query, (content_id,))

    return cursor.fetchall()[0]


@connection.connection_handler
def update_content(cursor: RealDictCursor, data):
    query = """UPDATE content
            SET title = %s, description = %s, public = %s, last_modified = %s, category = %s, image_source = %s
            WHERE id = %s
    """
    values = [data['title'], data['description'], data['public'], data['last_modified'], data['category'], data['image-source'], data['id']]
    if data['image-source'] == '':
        query = """UPDATE content SET title = %s, description = %s, public = %s, last_modified = %s, category = %s, 
        image_source = %s, image = ''
         WHERE id = %s"""
        values = [data['title'], data['description'], data['public'], data['last_modified'], data['category'],
                  data['image-source'], data['id']]

    cursor.execute(query, values)


@connection.connection_handler
def delete_content(cursor: RealDictCursor, content_id):
    query = """DELETE FROM content
               WHERE id = %s
        """

    cursor.execute(query, content_id)


@connection.connection_handler
def update_info(cursor: RealDictCursor, data):
    query = """UPDATE company_info
                SET name = %s, telephone_number = %s, email = %s, address = %s, description = %s
                WHERE id = 1
        """
    values = [data['name'], data['telephone_number'], data['email'], data['address'], data['description']]

    cursor.execute(query, values)
