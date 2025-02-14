#%%
from flask import Flask, request, jsonify
import psycopg2
import os

app = Flask(__name__)

# Database connection settings (will be set as environment variables)
PGHOST = os.getenv("PGHOST", "postgres.railway.internal")
PGDATABASE = os.getenv("PGDATABASE", "railway")
PGUSER = os.getenv("PGUSER", "postgres")
PGPASSWORD = os.getenv("PGPASSWORD", "WaFKDOwfsFjzjdaTybYboSrpUglKgrku")  
PGPORT = os.getenv("PGPORT", "5432")

# Connect to PostgreSQL
def get_db_connection():
    return psycopg2.connect(
        host=PGHOST,
        database=PGDATABASE,
        user=PGUSER,
        password=PGPASSWORD,
        port=PGPORT
    )

# Features for each plan
features = {
    "basic": ["Acute Coronary Syndrome", "FIPS 140-2",  "External Barcode Reader", "XML Format Output", 
 " Remote Applications", "Full Disclosure", "Network Printer"],
    "premium": ["Acute Coronary Syndrome", "FIPS 140-2", "12SL Precision", "External Barcode Reader", "XML Format Output", 
 " Remote Applications", "Full Disclosure", "Network Printer", "300Hz Acquisiton", "prior ECG", "Signal Averaged ECG", "global Wireless"]
}

@app.route("/subscription", methods=["GET"])
def get_subscription():
    user_id = request.args.get("user_id")

    if not user_id:
        return jsonify({"error": "User ID is required"}), 400

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT plan FROM users WHERE user_id = %s", (user_id,))
    user = cur.fetchone()
    cur.close()
    conn.close()

    if not user:
        return jsonify({"error": "User not found"}), 404

    plan = user[0]
    return jsonify({"user_id": user_id, "plan": plan, "features": features[plan]})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

# %%
