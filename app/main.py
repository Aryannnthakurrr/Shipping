from fastapi import FastAPI, status, HTTPException as http
from scalar_fastapi import get_scalar_api_reference
from .schemas import ShipmentCreate, ShipmentRead, ShipmentUpdate
from .database import save, shipments
 
app = FastAPI()


app.get("/scalar", include_in_schema=False)(
    lambda: get_scalar_api_reference(openapi_url="/openapi.json")
)


###  a shipment by id
@app.get("/shipment", response_model=ShipmentRead)
def get_shipment(id: int):
    # Check for shipment with given id
    if id not in shipments:
        raise http(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Given id doesn't exist!",
        )

    return shipments[id]


### Create a new shipment with content and weight
@app.post("/shipment", response_model=None)
def submit_shipment(shipment: ShipmentCreate) -> dict[str, int]:
    # Create and assign shipment a new id
    new_id = max(shipments.keys()) + 1
    # Add to shipments dict
    shipments[new_id] = {
        **shipment.model_dump(),
        "id": new_id,
        "status": "placed",
    }
    save()
    # Return id for later use
    return {"id": new_id}

#@app.patch("/shipment")
#def patch_shipment(
#    id: int, content: str | None = None, weight: float | None = None, status: str | None = None
#) -> dict[str, Any]:
#
#    if content is not None:
#        shipments[id]["content"] = content
#    if weight is not None:
#        shipments[id]["weight"] = weight
#    if status is not None:
#        shipments[id]["status"] = status
#    return shipments[id]

### Update fields of a shipment
@app.patch("/shipment", response_model=ShipmentRead)
def update_shipment(id: int, body: ShipmentUpdate):
    # Update data with given fields
    shipments[id].update(body.model_dump(exclude_none=True))
    save()
    return shipments[id]

### Delete a shipment by id
@app.delete("/shipment")
def delete_shipment(id: int) -> dict[str, str]:
    # Remove from datastore
    shipments.pop(id)

    return {"detail": f"Shipment with id #{id} is deleted!"}

