import uuid
from typing import List, Optional
from pydantic import BaseModel, Field
import uuid
from odmantic import EmbeddedModel, Model


class Review(Model):
    account_id: str
    review: str
    rating: float
    timestamp: str

    class Config:
        collection = "reviews"


class Listing(BaseModel):
    title: str = Field(...)
    display_images: List[str] = Field(...)
    views: int = Field(...)
    reference: str = Field(...)
    location: str = Field(...)
    account_id: str = Field(...)
    category_id: str = Field(...)
    additional_details: dict = Field(...)
    promoted: bool = Field(...)
    status: dict = Field(...)
    reviews: List[dict] = Field(...)
    
    class Config:
        allow_population_by_field_name = True
        
        schema_extra = {
            "example": {
                "_id": "f3r43-4f3r4-3f4r3-4f3r4",
                "title": "Don Quixote",
                "display_images": ["https://www.google.com", "https://www.google.com"],
                "views": 0,
                "reference": "123456",
                "location": "Madrid, Spain",
                "account_id": "f3r43-4f3r4-3f4r3-4f3r4",
                "category_id": "f3r43-4f3r4-3f4r3-4f3r4",
                "additional_details": {
                    "author": "Miguel de Cervantes",
                    "year": 1605,
                    "pages": 1000,
                },
                "promoted": "True",
                "status": "activated",
            }
        }


class ListingInDB(Model):
    account_id: str
    display_images: List[str]
    title: str
    views: int
    reference: str
    location: str
    category_id: str
    additional_details: dict
    promoted: bool
    status: str # (activated, unactivated, pending)
    created_at: str
    updated_at: str
    reports:list

    class Config:
        collection = "listings"


class ListingUpdate(BaseModel):
    title: Optional[str]
    country: Optional[str] 
    city: Optional[str] 
    promoted: Optional[bool] # can only changed by us
    status: Optional[str] # can only changed by us
    reports:list

    class Config:
        schema_extra = {
            "example": {
                "_id": "f3r43-4f3r4-3f4r3-4f3r4",
                "title": "Don Quixote",
                "country": "Spain",
                "city": "Madrid",   
                "promoted": "True",
                "status": "activated"
            }
        }


class ListingForm(BaseModel):
    title: str
    display_images: List[str] # handled by frontend after successful upload
    views: int 
    # reference: str
    location: str
    category_id: str
    additional_details: dict
    promoted: bool
    status: str # (activated, unactivated, pending)

    class Config:
        schema_extra = {
            "example": {
                "title": "Don Quixote",
                "display_images": ["https://www.google.com", "https://www.google.com"],
                "views": 0,
                "reference": "123456",
                "location": "Madrid, Spain",
                "category_id": "f3r43-4f3r4-3f4r3-4f3r4",
                "additional_details": {
                    "author": "Miguel de Cervantes",
                    "year": 1605,
                    "pages": 1000,
                },
                "promoted": "True",
                "status": "activated",
            }
        }


class ListingResponse(BaseModel):
    title: str
    display_images: List[str]
    views: int
    reference: str
    location: str
    category_id: str
    additional_details: dict
    promoted: bool
    status: str # (activated, unactivated, pending)
    created_at: str
    updated_at: str