import uuid
from typing import Optional
from pydantic import BaseModel, Field

class Listing(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    title: str = Field(...)
    country: str = Field(...)
    city: str = Field(...)
    promoted: bool = Field(...)
    status: str = Field(...) # activated, unactivated, pending)
  

    class Config:
        allow_population_by_field_name = True
        
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

                