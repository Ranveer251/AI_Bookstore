from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
from src.core.models import UnifiedBookModel

class BaseHarmonizer(ABC):
    """Base class for schema harmonizers"""
    
    def __init__(self, store_id: str, store_name: str):
        self.store_id = store_id
        self.store_name = store_name
    
    @abstractmethod
    def harmonize(self, raw_data: Dict[str, Any]) -> UnifiedBookModel:
        """Convert raw data to unified model"""
        pass
    
    @abstractmethod
    def get_schema_mapping(self) -> Dict[str, str]:
        """Return field mapping from source to unified schema"""
        pass
    
    def batch_harmonize(self, raw_data_list: List[Dict[str, Any]]) -> List[UnifiedBookModel]:
        """Harmonize a batch of records"""
        harmonized = []
        for raw_data in raw_data_list:
            try:
                unified_book = self.harmonize(raw_data)
                harmonized.append(unified_book)
            except Exception as e:
                print(f"Error harmonizing record: {e}")
                continue
        return harmonized