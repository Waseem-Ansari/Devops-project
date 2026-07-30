from flask import Flask, jsonify
import psycopg2
import os
 
app = Flask(__name__)
 
def get_db():
    # reads all config from environment variables
    # injected by kubernetes configmap and secret
    return psycopg2.connect(
        host=os.environ.get("DB_HOST"),
        database=os.environ.get("DB_NAME"),
        user=os.environ.get("DB_USER"),
        password=os.environ.get("DB_PASSWORD")
    )
 
@app.route("/")
def home():
    return jsonify({
        "message": "Flask on Kubernetes!",
        "environment": os.environ.get("APP_ENV", "production"),
        "version": "1.0"
    })
 
@app.route("/health")
def health():
    return jsonify({"status": "healthy"})
 
@app.route("/db-check")
def db_check():
    try:
        # test database connection
        conn = get_db()
        conn.close()
        return jsonify({"database": "connected ✅"})
    except Exception as e:
        return jsonify({
            "database": "failed ❌",
            "error": str(e)
        }), 500
 
@app.route("/engineers")
def engineers():
    try:
        conn = get_db()
        cur = conn.cursor()
 
        # create table if not exists
        cur.execute("""
            CREATE TABLE IF NOT EXISTS engineers
            (id SERIAL PRIMARY KEY, name VARCHAR(50))
        """)
 
        # insert a record
        cur.execute(
            "INSERT INTO engineers (name) VALUES (%s)",
            (os.environ.get("APP_ENV", "unknown") + " engineer",)
        )
        conn.commit()
 
        # fetch all records
        cur.execute("SELECT * FROM engineers")
        rows = cur.fetchall()
        cur.close()
        conn.close()
 
        return jsonify({"engineers": rows})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
 
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
