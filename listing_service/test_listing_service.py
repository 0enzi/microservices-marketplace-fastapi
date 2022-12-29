from fastapi import FastAPI
from fastapi.testclient import TestClient
from dotenv import dotenv_values
from pymongo import MongoClient
from routes import router as listing_router


"""
Listings:
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    title: str = Field(...)
    country: str = Field(...)
    city: str = Field(...)
    promoted: bool = Field(...)
    status: str = Field(...) # activated, unactivated, pending)
"""
app = FastAPI()
config = dotenv_values(".env")
app.include_router(listing_router, tags=["listings"], prefix="/listing")


@app.on_event("startup")
async def startup_event():
    app.mongodb_client = MongoClient(config["ATLAS_URI"])
    app.database = app.mongodb_client[config["DB_NAME"] + "test"]

@app.on_event("shutdown")
async def shutdown_event():
    app.mongodb_client.close()
    app.database.drop_collection("listings")

def test_create_listing():
    with TestClient(app) as client:
        response = client.post("/listing/", json={"title": "Don Quixote", "country": "Spain", "city": "Madrid", "promoted": "True", "status": "activated"})

        assert response.status_code == 201

        body = response.json()
        assert body.get("title") == "Don Quixote"
        assert body.get("country") == "Spain"
        assert body.get("city") == "Madrid"
        assert body.get("promoted") == "True"
        assert body.get("status") == "activated"
        assert "_id" in body


def test_create_listing_missing_title():
    with TestClient(app) as client:
        response = client.post("/listing/", json={"country": "Spain", "city": "Madrid", "promoted": "True", "status": "activated"})
        assert response.status_code == 422


def test_create_listing_missing_country():
    with TestClient(app) as client:
        response = client.post("/listing/", json={"title": "Don Quixote", "synopsis": "..."})
        assert response.status_code == 422


def test_create_listing_missing_city():
    with TestClient(app) as client:
        response = client.post("/listing/", json={"title": "Don Quixote", "author": "Miguel de Cervantes"})
        assert response.status_code == 422

def test_create_listing_missing_promoted():
    with TestClient(app) as client:
        response = client.post("/listing/", json={"title": "Don Quixote", "author": "Miguel de Cervantes"})
        assert response.status_code == 422

def test_create_listing_missing_status():
    with TestClient(app) as client:
        response = client.post("/listing/", json={"title": "Don Quixote", "author": "Miguel de Cervantes"})
        assert response.status_code == 422

def test_get_listing():
    with TestClient(app) as client:
        new_listing = client.post("/listing/", json={"country": "Spain", "city": "Madrid", "promoted": "True", "status": "activated"}).json()

        get_listing_response = client.get("/listing/" + new_listing.get("_id"))
        assert get_listing_response.status_code == 200
        assert get_listing_response.json() == new_listing


def test_get_listing_unexisting():
    with TestClient(app) as client:
        get_listing_response = client.get("/listing/unexisting_id")
        assert get_listing_response.status_code == 404


def test_update_listing():
    with TestClient(app) as client:
        new_listing = client.post("/listing/", json={"country": "Spain", "city": "Madrid", "promoted": "True", "status": "activated"}).json()

        response = client.put("/listing/" + new_listing.get("_id"), json={"title": "Don Quixote 1"})
        assert response.status_code == 200
        assert response.json().get("title") == "Don Quixote 1"


def test_update_listing_unexisting():
    with TestClient(app) as client:
        update_listing_response = client.put("/listing/unexisting_id", json={"title": "Don Quixote 1"})
        assert update_listing_response.status_code == 404


def test_delete_listing():
    with TestClient(app) as client:
        new_listing = client.post("/listing/", json={"country": "Spain", "city": "Madrid", "promoted": "True", "status": "activated"}).json()

        delete_listing_response = client.delete("/listing/" + new_listing.get("_id"))
        assert delete_listing_response.status_code == 204


def test_delete_listing_unexisting():
    with TestClient(app) as client:
        delete_listing_response = client.delete("/listing/unexisting_id")
        assert delete_listing_response.status_code == 404