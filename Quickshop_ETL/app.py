from flask import Flask, request, jsonify
import threading
import os
import logging
from datetime import datetime

from Quickshop_ETL.db import SessionLocal, engine
from Quickshop_ETL.models import OrderTransformed
from sqlalchemy import text

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)


# 🟢 Run ETL automatically once when Flask starts
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


# 🩺 Health Check
@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"}), 200


# 🔵 Get all orders
@app.route("/orders", methods=["GET"])
def get_orders():
    session = SessionLocal()
    try:
        orders = session.query(OrderTransformed).order_by(OrderTransformed.order_id).all()
        result = [
            {
                "order_id": o.order_id,
                "product_id": o.product_id,
                "qty": o.qty,
                "unit_price": float(o.unit_price),
                "order_total": float(o.order_total),
                "order_date": o.order_date.isoformat() if o.order_date else None
            }
            for o in orders
        ]
        return jsonify(result), 200
    except Exception as e:
        logging.error(f"❌ Error fetching orders: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        session.close()


# 🟢 Add new order
@app.route("/order", methods=["POST"])
def add_order():
    data = request.get_json()
    session = SessionLocal()
    try:
        order_total = data["qty"] * data["unit_price"]
        new_order = OrderTransformed(
            product_id=data["product_id"],
            qty=data["qty"],
            unit_price=data["unit_price"],
            order_total=order_total,
            order_date=datetime.strptime(data["order_date"], "%Y-%m-%d").date(),
        )
        session.add(new_order)
        session.commit()
        return jsonify({
            "message": "Order added successfully",
            "order_id": new_order.order_id
        }), 201
    except Exception as e:
        session.rollback()
        logging.error(f"❌ Error adding order: {e}")
        return jsonify({"error": str(e)}), 400
    finally:
        session.close()


# 🟡 Update existing order
@app.route("/orders/<int:order_id>", methods=["PUT"])
def update_order(order_id):
    data = request.get_json()
    session = SessionLocal()
    try:
        order = session.query(OrderTransformed).filter(OrderTransformed.order_id == order_id).first()
        if not order:
            return jsonify({"error": "Order not found"}), 404

        order.product_id = data["product_id"]
        order.qty = data["qty"]
        order.unit_price = data["unit_price"]
        order.order_total = data["qty"] * data["unit_price"]
        order.order_date = datetime.strptime(data["order_date"], "%Y-%m-%d").date()

        session.commit()
        return jsonify({"message": f"Order {order_id} updated successfully"}), 200
    except Exception as e:
        session.rollback()
        logging.error(f"❌ Error updating order: {e}")
        return jsonify({"error": str(e)}), 400
    finally:
        session.close()


# 🔴 Delete order
@app.route("/orders/<int:order_id>", methods=["DELETE"])
def delete_order(order_id):
    session = SessionLocal()
    try:
        order = session.query(OrderTransformed).filter(OrderTransformed.order_id == order_id).first()
        if not order:
            return jsonify({"error": "Order not found"}), 404

        session.delete(order)
        session.commit()
        return jsonify({"message": f"Order {order_id} deleted"}), 200
    except Exception as e:
        session.rollback()
        logging.error(f"❌ Error deleting order: {e}")
        return jsonify({"error": str(e)}), 400
    finally:
        session.close()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
