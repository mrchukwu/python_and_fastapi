from typing import Any

from fastapi import FastAPI, HTTPException, status
from scalar_fastapi import get_scalar_api_reference

from app.database import Database

# from app.database_json import shipments
from app.schemas import ShipmentCreate, ShipmentRead, ShipmentUpdate

app = FastAPI()
db = Database()


@app.post("/shipments")
def submit_shipment(shipment: ShipmentCreate) -> dict[str, int]:
    new_id = db.create(shipment)
    return {"id": new_id}


@app.get("/shipments/{id}", response_model=ShipmentRead)
def get_shipment(id: int) -> dict[str, Any]:
    shipment = db.get(id)
    if shipment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Given id {id} doesn't exist"
        )
    return shipment


@app.patch("/shipments/{id}", response_model=ShipmentRead)
def update_shipment(id: int, shipment: ShipmentUpdate):
    shipment = db.update(id, shipment)
    return shipment


@app.delete("/shipments/{id}")
def delete_shipment(id: int) -> dict[str, Any]:
    db.delete(id)
    return {
        "message": "shipment deleted successfully",
    }


@app.get("/health_check")
def health_check():
    return {"content": "Server running smoothly"}


@app.get("/scalar", include_in_schema=False)
def get_scalr_docs():
    return get_scalar_api_reference(openapi_url=app.openapi_url, title="Scalar API")


# @app.get("/shipment/latest")
# def get_latest_shipment():
#     id = max(shipments.keys())
#     return shipments[id]

# @app.get("/shipments")
# def get_all_shipments() -> dict[int, Any]:
#     return shipments

# @app.get("/shipments/{field}", response_model=ShipmentRead)
# def get_shipment_field(id: int, field: str) -> dict[str, Any]:
#     return {"field": shipments[id][field]}
