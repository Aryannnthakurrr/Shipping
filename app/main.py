from fastapi import FastAPI, status, HTTPException as http, Depends
from scalar_fastapi import get_scalar_api_reference
from contextlib import asynccontextmanager
from app.database.session import create_db_tables

from .schemas import ShipmentCreate, ShipmentRead, ShipmentUpdate
from .database import Database
 
@asynccontextmanager
async def lifespan_handler(app: FastAPI):
    create_db_tables()
    print("Server started")
    yield
    print("Server stopped")

app = FastAPI(lifespan=lifespan_handler)


def get_db():
    """Dependency: creates a new database instance per request and closes it after"""
    db = Database("sqlite.db")
    try:
        yield db
    finally:
        db.close()


app.get("/scalar", include_in_schema=False)(
    lambda: get_scalar_api_reference(openapi_url="/openapi.json")
)


###  a shipment by id
@app.get("/shipment", response_model=ShipmentRead)
def get_shipment(id: int, db: Database = Depends(get_db),):
    # Check for shipment with given id
    shipment = db.get(id)
    if shipment is None:
        raise http(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Given id doesn't exist!",
        )
    return shipment
    
### Create a new shipment with content and weight
@app.post("/shipment", response_model=None)
def submit_shipment(shipment: ShipmentCreate, db: Database = Depends(get_db)) -> dict[str, int]:
    new_id = db.create(shipment)
    # Return id for later use
    return {"id": new_id}

### Update fields of a shipment
@app.patch("/shipment", response_model=ShipmentRead)
def update_shipment(id: int, shipment: ShipmentUpdate, db: Database = Depends(get_db)):
    # Update data with given fields
    updated_shipment = db.update(id, shipment)
    return updated_shipment

### Delete a shipment by id
@app.delete("/shipment")
def delete_shipment(id: int, db: Database = Depends(get_db)) -> dict[str, str]:
    # Remove from datastore
    db.delete(id)
    return {"detail": f"Shipment with id #{id} is deleted!"}

