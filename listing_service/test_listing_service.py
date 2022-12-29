from fastapi import FastAPI
from fastapi.testclient import TestClient
from dotenv import dotenv_values
from pymongo import MongoClient
from routes import router as listing_router


"""
Listings:
     id: str = Field(default_factory=uuid.uuid4, alias="_id")
    title: str = Field(...)
    display_images: List[str] = Field(...)
    views: int = Field(...)
    reference: str = Field(...)
    location: str = Field(...)
    merchant_id: str = Field(...)
    category: str = Field(...)
    additional_details: str = Field(...)
    promoted: bool = Field(...)
    status: str = Field(...) # activated, unactivated, pending)
"""
app = FastAPI()
config = dotenv_values(".env")
app.include_router(listing_router, tags=["listings"], prefix="/listing")


@app.on_event("startup")
async def startup_event():
    # Initialize database when app starts
    app.mongodb_client = MongoClient(config["ATLAS_URI"])
    app.database = app.mongodb_client[config["DB_NAME"] + "test"]

@app.on_event("shutdown")
async def shutdown_event():
    # Close database connection when app shuts down
    app.mongodb_client.close()
    app.database.drop_collection("listings")

def test_create_listing():

    with TestClient(app) as client:
        response = client.post("/listing/", json={
            "title": "Don Quixote",
            "display_images": ["https://cdn.24.co.za/files/Cms/General/d/10899/6437b5a468da44f2a0e78b8b204d81f7.jpg", "https://cdn.24.co.za/files/Cms/General/d/10899/6437b5a468da44f2a0e78b8b204d81f7.jpg"],
             "views": 0,
                "reference": "123456789",
                "location": "Madrid",
                "merchant_id": "123456789",
                "category": "Books",
                "additional_details": {"pages": "1000", "language": "Spanish", "author": "Miguel de Cervantes"},         
               "promoted": "True",
                "status": "activated"
                })

        assert response.status_code == 201

        body = response.json()
        assert body.get("title") == "Don Quixote"
        assert body.get("display_images") == ["https://cdn.24.co.za/files/Cms/General/d/10899/6437b5a468da44f2a0e78b8b204d81f7.jpg", "https://cdn.24.co.za/files/Cms/General/d/10899/6437b5a468da44f2a0e78b8b204d81f7.jpg"]
        assert body.get("views") == 0
        assert body.get("reference") == "123456789"
        assert body.get("location") == "Madrid"
        assert body.get("merchant_id") == "123456789"
        assert body.get("category") == "Books"
        assert body.get("additional_details") == {"pages": "1000", "language": "Spanish", "author": "Miguel de Cervantes"}
        assert body.get("promoted") == "True"
        assert body.get("status") == "activated"
        assert "_id" in body
        

def test_create_listing_missing_title():
    with TestClient(app) as client:
        response = client.post("/listing/", json={
                "display_images": ["https://cdn.24.co.za/files/Cms/General/d/10899/6437b5a468da44f2a0e78b8b204d81f7.jpg", "https://cdn.24.co.za/files/Cms/General/d/10899/6437b5a468da44f2a0e78b8b204d81f7.jpg"],
                "views": 0,
                "reference": "123456789",
                "location": "Madrid",
                "merchant_id": "123456789",
                "category": "Books",
                "additional_details": {"pages": "1000", "language": "Spanish", "author": "Miguel de Cervantes"},
                "promoted": "True",
                "status": "activated",
                    })
        assert response.status_code == 422

def test_create_listing_missing_display_images():
    with TestClient(app) as client:
        response = client.post("/listing/", json={
                "title": "Don Quixote",
                "views": 0,
                "reference": "123456789",
                "location": "Madrid",
                "merchant_id": "123456789",
                "category": "Books",
                "additional_details": {"pages": "1000", "language": "Spanish", "author": "Miguel de Cervantes"},
                "promoted": "True",
                "status": "activated",
                    })
        assert response.status_code == 422

def test_create_listing_missing_views():
    with TestClient(app) as client:
        response = client.post("/listing/", json={
                "title": "Don Quixote",
                "display_images": ["https://cdn.24.co.za/files/Cms/General/d/10899/6437b5a468da44f2a0e78b8b204d81f7.jpg", "https://cdn.24.co.za/files/Cms/General/d/10899/6437b5a468da44f2a0e78b8b204d81f7.jpg"],
                "reference": "123456789",
                "location": "Madrid",
                "merchant_id": "123456789",
                "category": "Books",
                "additional_details": {"pages": "1000", "language": "Spanish", "author": "Miguel de Cervantes"},
                "promoted": "True",
                "status": "activated",
                    })
        assert response.status_code == 422

def test_create_listing_missing_reference():
    with TestClient(app) as client:
        response = client.post("/listing/", json={
                "title": "Don Quixote",
                "display_images": ["https://cdn.24.co.za/files/Cms/General/d/10899/6437b5a468da44f2a0e78b8b204d81f7.jpg", "https://cdn.24.co.za/files/Cms/General/d/10899/6437b5a468da44f2a0e78b8b204d81f7.jpg"],
                "views": 0,
                "location": "Madrid",
                "merchant_id": "123456789",
                "category": "Books",
                "additional_details": {"pages": "1000", "language": "Spanish", "author": "Miguel de Cervantes"},
                "promoted": "True",
                "status": "activated",
                    })
        assert response.status_code == 422

def test_create_listing_missing_location():
    with TestClient(app) as client:
        response = client.post("/listing/", json={
                "title": "Don Quixote",
                "display_images": ["https://cdn.24.co.za/files/Cms/General/d/10899/6437b5a468da44f2a0e78b8b204d81f7.jpg", "https://cdn.24.co.za/files/Cms/General/d/10899/6437b5a468da44f2a0e78b8b204d81f7.jpg"],
                "views": 0,
                "reference": "123456789",
                "merchant_id": "123456789",
                "category": "Books",
                "additional_details": {"pages": "1000", "language": "Spanish", "author": "Miguel de Cervantes"},
                "promoted": "True",
                "status": "activated",
                    })
        assert response.status_code == 422

def test_create_listing_missing_merchant_id():
    with TestClient(app) as client:
        response = client.post("/listing/", json={
                "title": "Don Quixote",
                "display_images": ["https://cdn.24.co.za/files/Cms/General/d/10899/6437b5a468da44f2a0e78b8b204d81f7.jpg", "https://cdn.24.co.za/files/Cms/General/d/10899/6437b5a468da44f2a0e78b8b204d81f7.jpg"],
                "views": 0,
                "reference": "123456789",
                "location": "Madrid",
                "category": "Books",
                "additional_details": {"pages": "1000", "language": "Spanish", "author": "Miguel de Cervantes"},
                "promoted": "True",
                "status": "activated",
                    })
        assert response.status_code == 422

def test_create_listing_missing_category():
    with TestClient(app) as client:
        response = client.post("/listing/", json={
                "title": "Don Quixote",
                "display_images": ["https://cdn.24.co.za/files/Cms/General/d/10899/6437b5a468da44f2a0e78b8b204d81f7.jpg", "https://cdn.24.co.za/files/Cms/General/d/10899/6437b5a468da44f2a0e78b8b204d81f7.jpg"],
                "views": 0,
                "reference": "123456789",
                "location": "Madrid",
                "merchant_id": "123456789",
                "additional_details": {"pages": "1000", "language": "Spanish", "author": "Miguel de Cervantes"},
                "promoted": "True",
                "status": "activated",
                    })
        assert response.status_code == 422

def test_create_listing_missing_additional_details():
    with TestClient(app) as client:
        response = client.post("/listing/", json={
                "title": "Don Quixote",
                "display_images": ["https://cdn.24.co.za/files/Cms/General/d/10899/6437b5a468da44f2a0e78b8b204d81f7.jpg", "https://cdn.24.co.za/files/Cms/General/d/10899/6437b5a468da44f2a0e78b8b204d81f7.jpg"],
                "views": 0,
                "reference": "123456789",
                "location": "Madrid",
                "merchant_id": "123456789",
                "category": "Books",
                "promoted": "True",
                "status": "activated",
                    })
        assert response.status_code == 422

def test_create_listing_missing_status():
    with TestClient(app) as client:
        response = client.post("/listing/", json={
                "title": "Don Quixote",
                "display_images": ["https://cdn.24.co.za/files/Cms/General/d/10899/6437b5a468da44f2a0e78b8b204d81f7.jpg", "https://cdn.24.co.za/files/Cms/General/d/10899/6437b5a468da44f2a0e78b8b204d81f7.jpg"],
                "views": 0,
                "reference": "123456789",
                "location": "Madrid",
                "merchant_id": "123456789",
                "category": "Books",
                "additional_details": {"pages": "1000", "language": "Spanish", "author": "Miguel de Cervantes"},
                "promoted": "True",
                    })
        assert response.status_code == 422

def test_get_listing():
    with TestClient(app) as client:
        new_listing = client.post("/listing/", json={
                "title": "Don Quixote",
                "display_images": ["https://cdn.24.co.za/files/Cms/General/d/10899/6437b5a468da44f2a0e78b8b204d81f7.jpg", "https://cdn.24.co.za/files/Cms/General/d/10899/6437b5a468da44f2a0e78b8b204d81f7.jpg"],
                "views": 0,
                "reference": "123456789",
                "location": "Madrid",
                "merchant_id": "123456789",
                "category": "Books",
                "additional_details": {"pages": "1000", "language": "Spanish", "author": "Miguel de Cervantes"},
                "promoted": "True",
                "status": "activated",
                
        }).json()

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
        new_listing = client.post("/listing/", json={
                "title": "Don Quixote",
                "display_images": ["https://cdn.24.co.za/files/Cms/General/d/10899/6437b5a468da44f2a0e78b8b204d81f7.jpg", "https://cdn.24.co.za/files/Cms/General/d/10899/6437b5a468da44f2a0e78b8b204d81f7.jpg"],
                "views": 0,
                "reference": "123456789",
                "location": "Madrid",
                "merchant_id": "123456789",
                "category": "Books",
                "additional_details": {"pages": "1000", "language": "Spanish", "author": "Miguel de Cervantes"},
                
        }).json()

        delete_listing_response = client.delete("/listing/" + new_listing.get("_id"))
        assert delete_listing_response.status_code == 204


def test_delete_listing_unexisting():
    with TestClient(app) as client:
        delete_listing_response = client.delete("/listing/unexisting_id")
        assert delete_listing_response.status_code == 404