import uuid
from typing import List, Optional
from pydantic import BaseModel, Field
import uuid
from odmantic import EmbeddedModel, Model


class Category(Model):
   title: str
   seo_tag_title: str
   seo_tag_description: str
   seo_tag_keywords: list
   sub_categories: list

   class Config:
        collection = "categories"

   
class SubCategory(Model):
    title: str
    slug: str
    description: str
    seo_tag_title: str
    seo_tag_description: str
    seo_tag_keywords: list
    active: str
    created_at: str
    updated_at: str
    listings: list
    sub_categories: list

    class Config:
        collection = "sub_categories"


class CategoryUpdate(BaseModel):
    name: str
    seo_tag_title: str
    seo_tag_description: str
    seo_tag_keywords: list
    sub_categories: list

    class Config:
        schema_extra = {
            "example": {
                "name": "Books",
                "seo_tag_title": "Books",
                "seo_tag_description": "Books",
                "seo_tag_keywords": ["Books", "Novels"],
                "sub_categories": ["f3r43-4f3r4-3f4r3-4f3r4", "f3r43-4f3r4-3f4r3-4f3r4"],
            }
        }


class SubCategoryUpdate(BaseModel):
    title: str
    slug: str
    description: str
    seo_tag_title: str
    seo_tag_description: str
    seo_tag_keywords: list
    active: str
    updated_at: str
    created_at: str

    class Config:
        schema_extra = {
            "example": {
                "title": "Don Quixote",
                "slug": "don-quixote",
                "description": "Don Quixote is a Spanish novel by Miguel de Cervantes Saavedra. Published in two volumes, in 1605 and 1615, Don Quixote is considered the most influential work of literature from the Spanish Golden Age and the entire Spanish literary canon. As a founding work of modern Western literature and one of the earliest canonical novels, it regularly appears high on lists of the greatest works of fiction ever published.",
                "seo_tag_title": "Don Quixote",
                "seo_tag_description": "Don Quixote is a Spanish novel by Miguel de Cervantes Saavedra. Published in two volumes, in 1605 and 1615, Don Quixote is considered the most influential work of literature from the Spanish Golden Age and the entire Spanish literary canon. As a founding work of modern Western literature and one of the earliest canonical novels, it regularly appears high on lists of the greatest works of fiction ever published.",
                "seo_tag_keywords": ["Don Quixote", "Miguel de Cervantes", "Spanish novel"],
                "active": "True",
                "updated_at": "1673175707",
                "created_at": "1673175707",
            }
        }


class CategoryUpdate(BaseModel):
    name: str
    seo_tag_title: str
    seo_tag_description: str
    seo_tag_keywords: list
    sub_categories: list

    class Config:
        schema_extra = {
            "example": {
                "name": "Books",
                "seo_tag_title": "Books",
                "seo_tag_description": "Books",
                "seo_tag_keywords": ["Books", "Novels"],
                "sub_categories": ["f3r43-4f3r4-3f4r3-4f3r4", "f3r43-4f3r4-3f4r3-4f3r4"],
            }
        }


class CategoryForm(BaseModel):
    name: str
    seo_tag_title: str
    seo_tag_description: str
    seo_tag_keywords: list
    sub_categories: list = []

    class Config:
        schema_extra = {
            "example": {
                "name": "Books",
                "seo_tag_title": "Books",
                "seo_tag_description": "Books",
                "seo_tag_keywords": ["Books", "Novels"],
                "sub_categories": [],
            }
        }


class SubCategoryForm(BaseModel):
    title: str
    description: str
    seo_tag_title: str
    seo_tag_description: str
    seo_tag_keywords: list
    listings: list = []
    sub_categories: list = []

    class Config:
        schema_extra = {
            "example": {
                "title": "Don Quixote",
                "description": "Don Quixote is a Spanish novel by Miguel de Cervantes Saavedra. Published in two volumes, in 1605 and 1615, Don Quixote is considered the most influential work of literature from the Spanish Golden Age and the entire Spanish literary canon. As a founding work of modern Western literature and one of the earliest canonical novels, it regularly appears high on lists of the greatest works of fiction ever published.",
                "seo_tag_title": "Don Quixote",
                "seo_tag_description": "Don Quixote is a Spanish novel by Miguel de Cervantes Saavedra. Published in two volumes, in 1605 and 1615, Don Quixote is considered the most influential work of literature from the Spanish Golden Age and the entire Spanish literary canon. As a founding work of modern Western literature and one of the earliest canonical novels, it regularly appears high on lists of the greatest works of fiction ever published.",
                "seo_tag_keywords": ["Don Quixote", "Miguel de Cervantes", "Spanish novel"],
                "listings": [],
                "sub_categories": [],
            }
        }


class CategoryResponse(BaseModel):
    _id: str
    name: str
    seo_tag_title: str
    seo_tag_description: str
    seo_tag_keywords: list
    sub_categories: list

    class Config:
        schema_extra = {
            "example": {
                "id": "f3r43-4f3r4-3f4r3-4f3r4",
                "name": "Books",
                "seo_tag_title": "Books",
                "seo_tag_description": "Books",
                "seo_tag_keywords": ["Books", "Novels"],
                "sub_categories": ["f3r43-4f3r4-3f4r3-4f3r4", "f3r43-4f3r4-3f4r3-4f3r4"],
            }
        }


class SubCategoryResponse(BaseModel):
    _id:str
    title: str
    slug: str
    description: str
    seo_tag_title: str
    seo_tag_description: str
    seo_tag_keywords: list
    active: str
    created_at: str
    updated_at: str
    listings: list
    sub_categories: list
