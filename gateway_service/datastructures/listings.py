import uuid
from typing import List, Optional
from pydantic import BaseModel, Field

class ListingForm(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    title: str = Field(...)
    display_images: list[str] = Field(...)
    views: int = Field(...)
    reference: str = Field(...)
    location: str = Field(...)
    account_id: str = Field(...)
    category_id: str = Field(...)
    additionalx_details: dict = Field(...)
    promoted: bool = Field(...)
    status: str = Field(...) # activated, unactivated, pending)
    

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


class ListingUpdate(BaseModel):
    title: Optional[str]
    country: Optional[str] 
    city: Optional[str] 
    promoted: Optional[bool] # can only changed by us
    status: Optional[str] # can only changed by us

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

                