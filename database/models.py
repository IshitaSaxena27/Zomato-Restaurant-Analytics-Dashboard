from sqlalchemy import text

from database.db_config import engine


# ==========================
# GET ALL RESTAURANTS
# ==========================

def get_all_restaurants():

    query = """
    SELECT *
    FROM restaurants
    """

    with engine.connect() as conn:

        result = conn.execute(
            text(query)
        )

        return result.fetchall()


# ==========================
# INSERT RESTAURANT
# ==========================

def add_restaurant(
        name,
        online_order,
        book_table,
        rate,
        votes,
        cost,
        restaurant_type
):

    query = """
    INSERT INTO restaurants
    (
    name,
    online_order,
    book_table,
    rate,
    votes,
    cost,
    restaurant_type
    )

    VALUES

    (
    :name,
    :online_order,
    :book_table,
    :rate,
    :votes,
    :cost,
    :restaurant_type
    )
    """

    with engine.begin() as conn:

        conn.execute(
            text(query),
            {
                "name": name,
                "online_order": online_order,
                "book_table": book_table,
                "rate": rate,
                "votes": votes,
                "cost": cost,
                "restaurant_type": restaurant_type
            }
        )


# ==========================
# DELETE RESTAURANT
# ==========================

def delete_restaurant(id):

    query = """
    DELETE FROM restaurants
    WHERE id=:id
    """

    with engine.begin() as conn:

        conn.execute(
            text(query),
            {"id": id}
        )


# ==========================
# SEARCH RESTAURANT
# ==========================

def search_restaurant(keyword):

    query = """
    SELECT *
    FROM restaurants
    WHERE name LIKE :keyword
    """

    with engine.connect() as conn:

        result = conn.execute(
            text(query),
            {
                "keyword":
                f"%{keyword}%"
            }
        )

        return result.fetchall()


# ==========================
# TOP RESTAURANTS
# ==========================

def get_top_restaurants():

    query = """
    SELECT *
    FROM restaurants
    ORDER BY rate DESC
    LIMIT 10
    """

    with engine.connect() as conn:

        result = conn.execute(
            text(query)
        )

        return result.fetchall()