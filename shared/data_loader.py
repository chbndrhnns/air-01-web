"""Data loading utilities for the salary calculator."""

import json
import os
from typing import Dict, List, Set
from pathlib import Path

from .models import SalaryEntry, CountryData


class SalaryDataLoader:
    """Handles loading and parsing of salary data from JSON file."""
    
    def __init__(self, data_file_path: str = None):
        if data_file_path is None:
            # Default to data/calculatorData.json relative to project root
            project_root = Path(__file__).parent.parent
            data_file_path = project_root / "data" / "calculatorData.json"
        
        self.data_file_path = Path(data_file_path)
        self._raw_data = None
        self._processed_data = None
    
    def load_raw_data(self) -> Dict:
        """Load raw JSON data from file."""
        if self._raw_data is None:
            with open(self.data_file_path, 'r', encoding='utf-8') as f:
                self._raw_data = json.load(f)
        return self._raw_data
    
    def get_processed_data(self) -> Dict[str, Dict[str, CountryData]]:
        """Get processed data as structured models."""
        if self._processed_data is None:
            raw_data = self.load_raw_data()
            self._processed_data = {}
            
            for country, languages in raw_data.items():
                self._processed_data[country] = {}
                for language, data in languages.items():
                    entries = [SalaryEntry(**entry) for entry in data['entries']]
                    self._processed_data[country][language] = CountryData(entries=entries)
        
        return self._processed_data
    
    def get_countries(self) -> List[str]:
        """Get list of all available countries."""
        data = self.get_processed_data()
        return list(data.keys())
    
    def get_languages(self, country: str = None) -> List[str]:
        """Get list of all available programming languages, optionally filtered by country."""
        data = self.get_processed_data()
        
        if country:
            return list(data.get(country, {}).keys())
        
        # Get all unique languages across all countries
        languages = set()
        for country_data in data.values():
            languages.update(country_data.keys())
        return list(languages)
    
    def get_experience_levels(self, country: str = None, language: str = None) -> List[str]:
        """Get list of all available experience levels, optionally filtered."""
        data = self.get_processed_data()
        experience_levels = set()
        
        if country and language:
            # Get experience levels for specific country and language
            country_data = data.get(country, {})
            language_data = country_data.get(language)
            if language_data:
                for entry in language_data.entries:
                    experience_levels.add(entry.category)
        else:
            # Get all experience levels across all data
            for country_data in data.values():
                for language_data in country_data.values():
                    for entry in language_data.entries:
                        experience_levels.add(entry.category)
        
        return list(experience_levels)
    
    def get_salary_data(self, country: str = None, language: str = None, experience: str = None) -> List[SalaryEntry]:
        """Get salary entries based on filters."""
        data = self.get_processed_data()
        results = []
        
        countries_to_check = [country] if country else data.keys()
        
        for country_name in countries_to_check:
            if country_name not in data:
                continue
                
            languages_to_check = [language] if language else data[country_name].keys()
            
            for language_name in languages_to_check:
                if language_name not in data[country_name]:
                    continue
                    
                for entry in data[country_name][language_name].entries:
                    if experience is None or entry.category == experience:
                        results.append(entry)
        
        return results