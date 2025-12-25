from flask import Flask, render_template_string
import os
import mysql.connector as mysql
from dotenv import load_dotenv

# Load env vars (local dev; systemd/k8s will inject them)
load_dotenv(dotenv_path="/home/ubuntu/.env")

app = Flask(__name__)

DB_USER = os.environ.get("DB_USER")
DB_PASSWORD = os.environ.get("DB_PASSWORD")
DB_HOST = os.environ.get("DB_HOST")
DB_NAME = os.environ.get("DB_NAME")

def connect_db():
    return mysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        port=3306
    )

@app.route("/")
def index():
    try:
        db = connect_db()
        cursor = db.cursor()

        # Write: record visit
        cursor.execute("INSERT INTO visits () VALUES ()")
        db.commit()

        # Read: total visits
        cursor.execute("SELECT COUNT(*) FROM visits")
        visit_count = cursor.fetchone()[0]

        cursor.close()
        db.close()

        html = """
        <!doctype html>
        <html>
          <head>
            <title>Ovia App</title>
            <style>
              body { font-family: Arial, sans-serif; margin: 40px; }
              h1 { color: #2c3e50; }
              .counter { font-size: 2em; color: #27ae60; }
            </style>
          </head>
          <body>
            <h1>Ovia Flask + MySQL App</h1>
            <p>Total page visits:</p>
            <div class="counter">{{ visits }}</div>
            <p>Refresh the page to increment the counter.</p>
          </body>
        </html>
        """

        return render_template_string(html, visits=visit_count)

    except mysql.Error as err:
        return f"<h2>Database error:</h2><pre>{err}</pre>", 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)

