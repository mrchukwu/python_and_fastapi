from typing import Any

from fastapi import FastAPI, HTTPException, status
from scalar_fastapi import get_scalar_api_reference

from app.database_json import save, shipments
from app.enum import ShipmentStatus
from app.schemas import ShipmentCreate, ShipmentRead, ShipmentUpdate

app = FastAPI()


# shipments = {
#     123: {"weight": 1.6, "content": "glassware", "status": "placed"},
#     124: {"weight": 1.1, "content": "books", "status": "shipped"},
#     125: {"weight": 3.4, "content": "furniture", "status": "in_transit"},
#     126: {"weight": 1.6, "content": "clothing", "status": "returned"},
# }


@app.get("/shipment/latest")
def get_latest_shipment():
    id = max(shipments.keys())
    return shipments[id]


@app.get("/shipments")
def get_all_shipments() -> dict[int, Any]:
    return shipments


@app.post("/shipments")
def submit_shipment(shipment: ShipmentCreate) -> dict[str, int]:
    new_id = max(shipments.keys()) + 1
    shipments[new_id] = {
        "id": new_id,
        **shipment.model_dump(),
        "status": ShipmentStatus.placed,
    }
    save()
    return {"id": new_id}


@app.get("/shipments/{id}", response_model=ShipmentRead)
def get_shipment(id: int) -> dict[str, Any]:
    if id not in shipments:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Given id {id} doesn't exist"
        )
    return shipments[id]


@app.patch("/shipments/{id}", response_model=ShipmentRead)
def update_shipment(id: int, body: ShipmentUpdate):
    if id not in shipments:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"{id} not found"
        )
    shipments[id].update(body.model_dump(exclude_none=True))
    save()
    return shipments[id]


@app.delete("/shipments/{id}")
def delete_shipment(id: int) -> dict[str, Any]:
    removed_shipment = shipments.pop(id)
    return {
        "message": f"shipment {shipments[id]} removed from shipments",
        "removed shipment": removed_shipment,
    }


@app.get("/shipments/{field}", response_model=ShipmentRead)
def get_shipment_field(id: int, field: str) -> dict[str, Any]:
    return {"field": shipments[id][field]}


@app.get("/health_check")
def health_check():
    return {"content": "Server running smoothly"}


@app.get("/scalar", include_in_schema=False)
def get_scalr_docs():
    return get_scalar_api_reference(openapi_url=app.openapi_url, title="Scalar API")
