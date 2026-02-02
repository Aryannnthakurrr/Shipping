import sqlite3
from typing import Any
from contextlib import contextmanager

from app.schemas import ShipmentCreate, ShipmentUpdate

class Database:

    def connect_to_db(self, db_path: str = "sqlite.db"):
        # Create a connection to the SQLite database (thread-safe per request)
        self.connection = sqlite3.connect(db_path)
        # Get cursor object to execute queries and fetch data
        self.cursor = self.connection.cursor()
        print("Connected to the database")

    def create_table(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS shipments(
                id INTEGER PRIMARY KEY,
                content TEXT,
                weight REAL,
                destination INTEGER,
                status TEXT 
            )
        """)

    def create(self, shipment: ShipmentCreate) -> int:
        # Find a new ID
        self.cursor.execute("SELECT MAX(id) FROM shipments")
        result = self.cursor.fetchone()

        new_id = (result[0] or 0) + 1
        # Insert values in the table
        self.cursor.execute("""
            INSERT INTO shipments 
            VALUES (:id, :content, :weight, :destination, :status)
        """, 
            {
                "id": new_id, 
                **shipment.model_dump(),
                "status": "placed"
            }
        )
        # Commit changes
        self.connection.commit()
        return new_id

    def get(self, id: int) -> dict[str, Any] | None:
        self.cursor.execute("SELECT * FROM shipments WHERE id = ?", (id,))
        row = self.cursor.fetchone()
        
        return {
            "id": row[0],
            "content": row[1],
            "weight": row[2],
            "destination": row[3],
            "status": row[4],
        } if row else None

    def update(self,id: int, shipment: ShipmentUpdate) -> dict[str, Any] | None:
        update_data = shipment.model_dump(exclude_unset=True)
        set_clause = ", ".join([f"{k} = :{k}" for k in update_data.keys()])
        
        self.cursor.execute(f"""
            UPDATE shipments SET {set_clause}
            WHERE id = :id
        """,
           {
                "id": id,
                **update_data
           }
        )
        self.connection.commit()

        return self.get(id)

    def delete(self, id: int):
        self.cursor.execute("DELETE FROM shipments WHERE id = ?", (id,))
        self.connection.commit()

        return {"detail": f"Shipment with id #{id} is deleted!"}

    def close(self):
        """Close the database connection"""
        print("....Closing database connection")
        self.connection.close()
        print("Database connection closed")

    # def __enter__(self):
    #     print("Entering database context")
    #     self.connect_to_db()
    #     self.create_table()
    #     return self

    # def __exit__(self, *arg):
    #     print("Exiting database context")
    #     self.close()

@contextmanager
def managed_db():
    db = Database()
    # Setup
    print("Entering database context")
    db.connect_to_db()
    db.create_table()

    yield db

    print("Exiting database context")

    # Teardown
    db.close()



with managed_db() as db:
    print(db.get(1))



