import uuid
from typing import List, Optional
from pydantic import BaseModel, Field
import uuid
from odmantic import EmbeddedModel, Model


class Report(BaseModel):
    account_id: str # reporting user
    description: str # extra info 


class ReportInDB(Model):
    account_id: str
    description: str

    class Config:
        collection = "reports"


class ReportUpdate(BaseModel):
    account_id: str
    description: str


class ReportForm(BaseModel):
    account_id: str
    description: str


class ReportResponse(BaseModel):
    account_id: str
    description: str