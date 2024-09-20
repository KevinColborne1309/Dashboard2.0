from flask import Flask, jsonify, render_template, Response, abort, make_response
import sqlite3
import pathlib
import logging

# Setup logging
logging.basicConfig(filename="app.log", level=logging.DEBUG)

working_directory = pathlib.Path(__file__).parent.absolute()
DATABASE = working_directory / "CSS8database.db" 

def query_db(query: str, args=()) -> list:
    try:
        with sqlite3.connect(DATABASE) as conn:
            cursor = conn.cursor()
            result = cursor.execute(query, args).fetchall()
        return result
    except sqlite3.Error as e:
        logging.error("Database error: %s", e)
        abort(500, description="Database error occurred.")

app = Flask(__name__)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({"error": "Not found"}), 404)

@app.errorhandler(500)
def internal_error(error):
    return make_response(jsonify({"error": "Internal server error"}), 500)

@app.route("/")
def index() -> str:
    return render_template("dashboard.html")

@app.route("/api/gender_distribution")
def gender_distribution() -> Response:
    query = """
    SELECT Gender, COUNT(*) AS count
    FROM your_table_name
    GROUP BY Gender;
    """
    result = query_db(query)
    genders = [row[0] for row in result]
    counts = [row[1] for row in result]
    return jsonify({"genders": genders, "counts": counts})

@app.route("/api/age_group_distribution")
def age_group_distribution() -> Response:
    query = """
    SELECT 
        CASE 
            WHEN Age = 'Under 25' THEN 'Under 25'
            WHEN Age = '25-49' THEN '25-49'
            WHEN Age = '50-65' THEN '50-65'
            ELSE 'Unknown'
        END AS age_group, COUNT(*) AS count
    FROM your_table_name
    GROUP BY age_group;
    """
    result = query_db(query)
    age_groups = [row[0] for row in result]
    counts = [row[1] for row in result]
    return jsonify({"age_groups": age_groups, "counts": counts})

@app.route("/api/a1_score_trends")
def a1_score_trends() -> Response:
    query = """
    SELECT Wave, Provider, AVG([A1 Score]) AS avg_score
    FROM your_table_name
    GROUP BY Wave, Provider
    ORDER BY Wave;
    """
    result = query_db(query)
    waves = sorted(list(set(row[0] for row in result)))
    providers = sorted(list(set(row[1] for row in result)))
    data = {provider: [0] * len(waves) for provider in providers}
    
    for row in result:
        wave_index = waves.index(row[0])
        data[row[1]][wave_index] = row[2]

    return jsonify({"waves": waves, "data": data})

if __name__ == "__main__":
    app.run(debug=True, port=5004)
