from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import List, Tuple
import pandas as pd

@dataclass
class FeatureArtifact:
    feature_category: str
    features_created: List[str]
    execution_time_ms: float
    missing_values_created: int = 0

class BaseFeatureBuilder(ABC):
    """
    Abstract base class for all Feature Builders.
    Follows the Strategy Pattern / Open-Closed Principle.
    """
    
    @abstractmethod
    def transform(self, df_aggregated: pd.DataFrame, df_raw: pd.DataFrame = None) -> Tuple[pd.DataFrame, FeatureArtifact]:
        """
        Applies behavioral feature engineering to the aggregated customer dataframe.
        
        Args:
            df_aggregated: The customer-level dataframe coming from CustomerAggregation.
            df_raw: Optional transaction-level dataframe if raw events are needed for calculation.
            
        Returns:
            Tuple[pd.DataFrame, FeatureArtifact]: The transformed dataframe and execution metadata.
        """
        pass
