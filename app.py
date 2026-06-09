from flask import (
    Flask,
    render_template,
    request,
    redirect,
    session,
    send_file
)

import pandas as pd
from sqlalchemy import text

from database.db_config import engine

from analysis.charts import generate_charts
from analysis.insights import get_dashboard_stats
from analysis.recommendation import (
    recommend_restaurants,
    top_restaurants,
    best_value_restaurants
)
from analysis.pdf_report import generate_pdf_report

app = Flask(__name__)

app.secret_key = "Ishita_Zomato_AI_2026_Project"


# ==========================
# LOGIN
# ==========================

@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':

        print("FORM SUBMITTED")

        username = request.form['username']
        password = request.form['password']

        print("USERNAME:", username)
        print("PASSWORD:", password)

        query = """
        SELECT *
        FROM users
        WHERE username=:username
        AND password=:password
        """

        with engine.connect() as conn:

            result = conn.execute(
                text(query),
                {
                    "username": username,
                    "password": password
                }
            )

            user = result.fetchone()

        print("USER FOUND:", user)

        if user:

            session["logged_in"] = True

            print("LOGIN SUCCESS")

            return redirect('/')

        else:

            print("LOGIN FAILED")

    return render_template('login.html')

# ==========================
# LOGOUT
# ==========================

@app.route('/logout')
def logout():

    session.clear()

    return redirect('/login')


# ==========================
# DASHBOARD
# ==========================

@app.route('/')
def dashboard():

    if not session.get("logged_in"):

        return redirect('/login')

    query = """
    SELECT *
    FROM restaurants
    """

    df = pd.read_sql(query, engine)

    stats = get_dashboard_stats(df)

    generate_charts(df)

    return render_template(
        "dashboard.html",
        total_restaurants=stats["total_restaurants"],
        avg_rating=stats["avg_rating"],
        total_votes=stats["total_votes"],
        avg_cost=stats["avg_cost"],
        top_restaurant=stats["top_restaurant"]
    )


# ==========================
# VIEW RESTAURANTS
# ==========================

@app.route('/restaurants')
def restaurants():

    query = """
    SELECT *
    FROM restaurants
    ORDER BY votes DESC
    LIMIT 500
    """

    df = pd.read_sql(
        query,
        engine
    )

    restaurants = df.to_dict(
        orient='records'
    )

    return render_template(
        "restaurants.html",
        restaurants=restaurants
    )

# ==========================
# ADD RESTAURANT
# ==========================

@app.route('/add', methods=['GET', 'POST'])
def add_restaurant():

    if not session.get("logged_in"):

        return redirect('/login')

    if request.method == 'POST':

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
                    "name": request.form["name"],
                    "online_order": request.form["online_order"],
                    "book_table": request.form["book_table"],
                    "rate": request.form["rate"],
                    "votes": request.form["votes"],
                    "cost": request.form["cost"],
                    "restaurant_type": request.form["restaurant_type"]
                }
            )

        return redirect('/restaurants')

    return render_template(
        "add_restaurant.html"
    )


# ==========================
# DELETE RESTAURANT
# ==========================

@app.route('/delete/<int:id>')
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

    return redirect('/restaurants')


# ==========================
# SEARCH
# ==========================

@app.route('/search', methods=['GET', 'POST'])
def search():

    results = []

    if request.method == 'POST':

        keyword = request.form['keyword']

        query = """
        SELECT *
        FROM restaurants
        WHERE name LIKE :keyword
        """

        df = pd.read_sql(
            text(query),
            engine,
            params={
                "keyword":
                f"%{keyword}%"
            }
        )

        results = df.to_dict(
            orient='records'
        )

    return render_template(
        "search.html",
        results=results
    )


# ==========================
# AI RECOMMENDATION
# ==========================

@app.route('/recommend', methods=['GET', 'POST'])
def recommend():

    recommendations = None

    if request.method == 'POST':

        budget = int(
            request.form['budget']
        )

        restaurant_type = (
            request.form['restaurant_type']
        )

        query = """
        SELECT *
        FROM restaurants
        """

        df = pd.read_sql(
            query,
            engine
        )

        recommendations = (
            recommend_restaurants(
                df,
                budget,
                restaurant_type
            )
        )

        recommendations = (
            recommendations.to_dict(
                orient='records'
            )
        )

    return render_template(
        'recommend.html',
        recommendations=recommendations
    )


# ==========================
# REPORTS
# ==========================

@app.route('/reports')
def reports():

    query = """
    SELECT *
    FROM restaurants
    """

    df = pd.read_sql(
        query,
        engine
    )

    top_data = (
        top_restaurants(df)
        .head(10)
        .to_dict(
            orient='records'
        )
    )

    best_value = (
        best_value_restaurants(df)
        .to_dict(
            orient='records'
        )
    )

    return render_template(
        'reports.html',
        top_restaurants=top_data,
        best_value=best_value
    )


# ==========================
# PDF REPORT
# ==========================

@app.route('/download-report')
def download_report():

    query = """
    SELECT *
    FROM restaurants
    """

    df = pd.read_sql(
        query,
        engine
    )

    stats = get_dashboard_stats(df)

    generate_pdf_report(
        stats["total_restaurants"],
        stats["avg_rating"],
        stats["total_votes"],
        stats["avg_cost"]
    )

    return send_file(
        "static/reports/zomato_report.pdf",
        as_attachment=True
    )


# ==========================
# MAIN
# ==========================

if __name__ == "__main__":

    app.run(
        debug=True
    )