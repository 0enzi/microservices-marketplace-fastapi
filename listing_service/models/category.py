import uuid
from typing import List, Optional
from pydantic import BaseModel, Field
import uuid
from odmantic import EmbeddedModel, Model


class Category(Model):
   title: str
   slug: str
   description: str
   seo_tag_title: str
   seo_tag_description: str
   seo_tag_keywords: list
   active: str
       
   
class CategoryInDB(Model):
    title: str
    slug: str
    description: str
    seo_tag_title: str
    seo_tag_description: str
    seo_tag_keywords: list
    active: str
    created_at: str
    updated_at: str

    class Config:
        collection = "categories"


class CategoryUpdate(BaseModel):
    title: str
    slug: str
    description: str
    seo_tag_title: str
    seo_tag_description: str
    seo_tag_keywords: list
    active: str
    updated_at: str

    class Config:
        schema_extra = {
            "example": {
                "title": "Don Quixote",
                "slug": "don-quixote",
                "description": "Don Quixote is a Spanish novel by Miguel de Cervantes Saavedra. Published in two volumes, in 1605 and 1615, Don Quixote is considered the most influential work of literature from the Spanish Golden Age and the entire Spanish literary canon. As a founding work of modern Western literature and one of the earliest canonical novels, it regularly appears high on lists of the greatest works of fiction ever published, such as the Bokklubben World Library list of the 100 best books of all time.",
                "seo_tag_title": "Don Quixote",
                "seo_tag_description": "Don Quixote is a Spanish novel by Miguel de Cervantes Saavedra. Published in two volumes, in 1605 and 1615, Don Quixote is considered the most influential work of literature from the Spanish Golden Age and the entire Spanish literary canon. As a founding work of modern Western literature and one of the earliest canonical novels, it regularly appears high on lists of the greatest works of fiction ever published, such as the Bokklubben World Library list of the 100 best books of all time.",
                "seo_tag_keywords": ["Don Quixote", "Miguel de Cervantes", "Spanish novel"],
                "active": "True",
            }
        }


class CategoryForm(BaseModel):
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


class CategoryResponse(BaseModel):
    account_info: dict
    username: str
    email: str
    phone: str 
    location: str
    created_at: str
    account_type_id: str
    is_super_admin: bool
    status: bool
    email_verified: bool
    phone_verified: bool
    following_categories: list
    following_list: list

