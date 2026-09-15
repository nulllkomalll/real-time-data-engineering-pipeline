import psycopg2
import random
import time
import json
import os

# Sample data
NAMES = [
    "Youness Khayour", "Dr. Amine Bensaid", "Dr. Tajjeeddine Rachidi",
    "Dr. Mhammecd Chraibi",
]
PRODUCTS = ["Laptops", "Office Desks", "Book Shelves", "Boat", "Rolls Royce Car"]
STATUSES = ["In Progress", "Delivered"]

# give the database a moment to start
time.sleep(5)

# KEY *** Connects to PostgreSQL via Docker service name db_service.
conn = psycopg2.connect(
    dbname="db",
    user="postgres",
    password="admin",
    host="db_service",   # <-- Docker service
    port="5432"          # <-- Container port
)
conn.autocommit = True
cursor = conn.cursor()

# 1) Ensure table exists
cursor.execute("""
    CREATE TABLE IF NOT EXISTS orders (
      order_id     SERIAL PRIMARY KEY,
      customer_name TEXT,
      product       TEXT,
      quantity      INTEGER,
      order_status  TEXT
    );
""")

def insert_order():
    name     = random.choice(NAMES)
    product  = random.choice(PRODUCTS)
    quantity = random.randint(1, 10)
    status   = random.choice(STATUSES)
    cursor.execute("""
        INSERT INTO orders (customer_name, product, quantity, order_status)
        VALUES (%s, %s, %s, %s)
    """, (name, product, quantity, status))
    print(f"✅ INSERTED: {name} – {product} – {quantity} – {status}")

def update_order():
    cursor.execute("SELECT order_id FROM orders ORDER BY RANDOM() LIMIT 1")
    row = cursor.fetchone()
    if not row:
        print("⚠️ No orders to update.")
        return
    order_id  = row[0]
    new_status = random.choice(STATUSES)
    cursor.execute("""
        UPDATE orders SET order_status = %s WHERE order_id = %s
    """, (new_status, order_id))
    print(f"🔁 UPDATED order_id {order_id} → {new_status}")

def delete_order():
    cursor.execute("SELECT order_id FROM orders ORDER BY RANDOM() LIMIT 1")
    row = cursor.fetchone()
    if not row:
        print("⚠️ No orders to delete.")
        return
    order_id = row[0]
    cursor.execute("DELETE FROM orders WHERE order_id = %s", (order_id,))
    print(f"❌ DELETED order_id {order_id}")

def run_tests():
    weights = [0.6, 0.2, 0.2]  # insert, update, delete
    actions = random.choices(["insert", "update", "delete"], weights=weights, k=10)
    for action in actions:
        if action == "insert":
            insert_order()
        elif action == "update":
            update_order()
        else:
            delete_order()
        time.sleep(2)  # give Debezium/Kafka time to pick up each change

sink_path = "sink/changes.json"

if __name__ == "__main__":
    try:
        run_tests()
    except Exception as e:
            print(f"⚠️  Error during tests: {e}")
    finally:
        # 2) Fetch the entire table as JSON
        cursor.execute("""
            SELECT order_id, customer_name, product, quantity, order_status
            FROM orders
            ORDER BY order_id
        """)
        rows = cursor.fetchall()
        orders = [
            {
                    "order_id":       r[0],
                    "customer_name":  r[1],
                    "product":        r[2],
                    "quantity":       r[3],
                    "order_status":   r[4]
            }
            for r in rows
        ]

        # 3) Append into sink/changes.json on the host
        sink_path = "sink/changes.json"
            # load existing
        try:
            with open(sink_path, "r") as f:
                    existing = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            existing = []

        combined = existing + orders

        with open(sink_path, "w") as f:
            json.dump(combined, f, indent=4)
        print(f"💾 Appended {len(orders)} records; file now has {len(combined)} total.")

    cursor.close()
    conn.close()


