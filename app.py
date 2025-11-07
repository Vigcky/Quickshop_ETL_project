from flask import Flask, request, jsonify
import psycopg2
from psycopg2.extras import RealDictCursor
import threading
import os
import logging

app = Flask(__name__)

@app.before_first_request
def run_etl_on_startup():
    """Run ETL automatically once when Flask starts."""
    def run_etl():
        logging.info("🚀 Starting ETL pipeline automatically...")
        exit_code = os.system(
            "python run_etl.py "
            "--input-dir data --output-dir out "
            "--start-date 2025-11-01 --end-date 2025-11-05 "
            "--format db "
            "--db-url postgresql+psycopg2://postgres:182003@postgres:5432/quickshop"
        )
        if exit_code == 0:
            logging.info("✅ ETL completed successfully!")
        else:
            logging.error("❌ ETL failed with exit code %s", exit_code)

    threading.Thread(target=run_etl, daemon=True).start()

def get_db_conn():
    return psycopg2.connect(
        host="postgres",     
        port=5432,
        dbname="quickshop",
        user="postgres",
        password="182003"
    )

#🟢
@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"}), 200

#🔵
@app.route("/orders", methods=["GET"])
def get_orders():
    conn = get_db_conn()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("SELECT * FROM orders_transformed ORDER BY order_id;")
    orders = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(orders), 200

#🟢
@app.route("/order", methods=["POST"])
def add_order():
    try:
        data = request.json
        conn = get_db_conn()
        cur = conn.cursor()
        order_total = data["qty"] * data["unit_price"]
        cur.execute("""
            INSERT INTO orders_transformed (product_id, qty, unit_price, order_total, order_date)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING order_id;
        """, (
            data["product_id"],
            data["qty"],
            data["unit_price"],
            order_total,
            data["order_date"]
        ))
        new_id = cur.fetchone()[0]
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({
            "message": "Order added successfully",
            "order_id": new_id
        }), 201
    except Exception as e:
        print(f"Error adding order: {e}")
        return jsonify({"error": str(e)}), 400


#🟡
@app.route("/orders/<int:order_id>", methods=["PUT"])
def update_order(order_id):
    data = request.json
    conn = get_db_conn()
    cur = conn.cursor()
    order_total = data["qty"] * data["unit_price"]
    cur.execute("""
        UPDATE orders_transformed
        SET product_id=%s, qty=%s, unit_price=%s, order_total=%s, order_date=%s
        WHERE order_id=%s;
    """, (data["product_id"], data["qty"], data["unit_price"], order_total, data["order_date"], order_id))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"message": f"Order {order_id} updated"}), 200

#🔴
@app.route("/orders/<int:order_id>", methods=["DELETE"])
def delete_order(order_id):
    conn = get_db_conn()
    cur = conn.cursor()
    cur.execute("DELETE FROM orders_transformed WHERE order_id = %s;", (order_id,))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"message": f"Order {order_id} deleted"}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
