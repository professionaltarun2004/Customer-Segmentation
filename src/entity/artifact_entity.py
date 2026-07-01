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
