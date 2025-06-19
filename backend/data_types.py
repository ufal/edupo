#!/usr/bin/env python3
#coding: utf-8

from typing import Optional, Literal, List
from pydantic import BaseModel, Field, constr

class GenerationParameters(BaseModel):
    rhyme_scheme: Optional[constr(pattern=r'^[A-Z]+$')] = Field(default=None)
    metre: Optional[Literal['J', 'T', 'D', 'N']] = Field(default=None)
    verses_count: int = Field(default=None, ge=2, le=20)
    syllables_count: int = Field(default=None, ge=1, le=20)
    first_words: List[str] = Field(default_factory=list)
    year: int = Field(default=1900)
    temperature: float = Field(default=1.0, ge=0.01, le=10.0)
    anaphors: List[str] = Field(default_factory=list)
    epanastrophes: List[str] = Field(default_factory=list)
    title: str = Field(default='Bez názvu')
    author_name: str = Field(default=None)
    max_strophes: int = Field(default=2, ge=1, le=20)
    modelspec: Literal['tm', 'mc'] = Field(default='tm')

if __name__=="__main__":
    print(GenerationParameters.schema_json(indent=2))

