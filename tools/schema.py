from pydantic import BaseModel, HttpUrl, Field
from typing import List, Optional

class Language(BaseModel):
    name: str = Field(..., description="Canonical language name")
    aliases: List[str] = Field(default_factory=list)
    evidence_url: HttpUrl

class Program(BaseModel):
    title: str
    origin_url: HttpUrl
    filename_ext: str = Field(..., description="e.g., .py, .c, .rb")
    code: str
    license_guess: Optional[str] = None

class Proposal(BaseModel):
    language: Language
    program: Program
