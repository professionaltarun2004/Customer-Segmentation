from dataclasses import dataclass
import pandas as pd

@dataclass
class DataIngestionArtifact:
    dataframe: pd.DataFrame
    rows: int
    columns: int
    source_path: str

@dataclass
class DataValidationArtifact:
    cleaned_dataframe: pd.DataFrame
    initial_rows: int
    final_rows: int
    dropped_rows: int

@dataclass
class DataCleaningArtifact:
    cleaned_dataframe: pd.DataFrame
    initial_rows: int
    final_rows: int
    dropped_rows: int

@dataclass
class CustomerAggregationArtifact:
    aggregated_dataframe: pd.DataFrame
    total_customers: int


from src.components.features.base import FeatureArtifact

@dataclass
class FeatureEngineeringArtifact:
    feature_dataframe: pd.DataFrame
    feature_artifacts: List[FeatureArtifact]

