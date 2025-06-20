"""FastAPI backend for the salary calculator application."""

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
import statistics
import sys
import os

# Add the parent directory to sys.path to import shared modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from shared.models import SalaryEntry, SalaryFilters, SalaryStats
from shared.data_loader import SalaryDataLoader

app = FastAPI(
    title="Salary Calculator API",
    description="API for JetBrains Developer Ecosystem Survey 2024 salary data",
    version="1.0.0"
)

# Configure CORS to allow Streamlit frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8501", "http://127.0.0.1:8501"],  # Streamlit default ports
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize data loader
data_loader = SalaryDataLoader()


@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "message": "Salary Calculator API",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/countries", response_model=List[str])
async def get_countries():
    """Get list of all available countries."""
    try:
        return data_loader.get_countries()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error loading countries: {str(e)}")


@app.get("/languages", response_model=List[str])
async def get_languages(country: Optional[str] = Query(None, description="Filter languages by country")):
    """Get list of all available programming languages, optionally filtered by country."""
    try:
        return data_loader.get_languages(country=country)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error loading languages: {str(e)}")


@app.get("/experience-levels", response_model=List[str])
async def get_experience_levels(
    country: Optional[str] = Query(None, description="Filter by country"),
    language: Optional[str] = Query(None, description="Filter by programming language")
):
    """Get list of all available experience levels, optionally filtered."""
    try:
        return data_loader.get_experience_levels(country=country, language=language)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error loading experience levels: {str(e)}")


@app.get("/salary-data", response_model=List[SalaryEntry])
async def get_salary_data(
    country: Optional[str] = Query(None, description="Filter by country"),
    language: Optional[str] = Query(None, description="Filter by programming language"),
    experience: Optional[str] = Query(None, description="Filter by experience level")
):
    """Get salary entries based on filters."""
    try:
        return data_loader.get_salary_data(
            country=country,
            language=language,
            experience=experience
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error loading salary data: {str(e)}")


@app.get("/salary-stats", response_model=SalaryStats)
async def get_salary_stats(
    country: Optional[str] = Query(None, description="Filter by country"),
    language: Optional[str] = Query(None, description="Filter by programming language"),
    experience: Optional[str] = Query(None, description="Filter by experience level")
):
    """Get aggregated salary statistics based on filters."""
    try:
        salary_entries = data_loader.get_salary_data(
            country=country,
            language=language,
            experience=experience
        )
        
        if not salary_entries:
            raise HTTPException(status_code=404, detail="No salary data found for the given filters")
        
        salaries = [entry.value for entry in salary_entries]
        
        return SalaryStats(
            min_salary=min(salaries),
            max_salary=max(salaries),
            median_salary=statistics.median(salaries),
            average_salary=statistics.mean(salaries),
            count=len(salaries)
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error calculating salary stats: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)