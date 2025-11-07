from sqlalchemy.orm import Session
from .db import SessionLocal
from .models import OrderTransformed
import logging

def write_to_db(df, if_exists="replace"):
    session: Session = SessionLocal()
    try:
        if if_exists == "replace":
            session.query(OrderTransformed).delete()

        records = [
            OrderTransformed(
                product_id=row["product_id"],
                qty=row["qty"],
                unit_price=row["unit_price"],
                order_total=row["order_total"],
                order_date=row["order_date"],
            )
            for _, row in df.iterrows()
        ]

        session.add_all(records)
        session.commit()
        logging.info(f"Wrote {len(records)} records to orders_transformed")

    except Exception as e:
        session.rollback()
        logging.error(f" DB insert failed: {e}")
        raise
    finally:
        session.close()
