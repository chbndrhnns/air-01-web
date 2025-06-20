"""Shared data models for the salary calculator application."""

from typing import Dict, List, Optional
from pydantic import BaseModel


class SalaryEntry(BaseModel):
    """Represents a single salary data entry."""
    value: int
    category: str
    metadata: Dict[str, str]


class CountryData(BaseModel):
    """Represents salary data for a country and language combination."""
    entries: List[SalaryEntry]


class SalaryFilters(BaseModel):
    """Represents filters for salary data queries."""
    country: Optional[str] = None
    language: Optional[str] = None
    experience: Optional[str] = None


class SalaryStats(BaseModel):
    """Represents aggregated salary statistics."""
    min_salary: int
    max_salary: int
    median_salary: float
    average_salary: float
    count: int