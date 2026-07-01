import sys
from pathlib import Path
import pandas as pd
from src.logger import logger
from src.exception import CustomException
from src.entity.config_entity import DataIngestionConfig
from src.entity.artifact_entity import DataIngestionArtifact

class DataIngestion:
    """
    DataIngestion component responsible for loading data from a given source path.
    Supports CSV and Excel files.
    """
    def __init__(self, config: DataIngestionConfig):
        self.config = config

    def initiate_data_ingestion(self) -> DataIngestionArtifact:
        """
        Reads the data from the configured path, validates its existence,
        and returns a DataIngestionArtifact.
        """
        logger.info("Starting data ingestion process.")
        try:
            file_path = Path(self.config.raw_data_path)
            
            if not file_path.exists():
                raise FileNotFoundError(f"File not found at: {file_path}")
            
            logger.info(f"Reading dataset from: {file_path}")
            
            extension = file_path.suffix.lower()
            if extension == '.csv':
                df = pd.read_csv(file_path)
            elif extension in ['.xlsx', '.xls']:
                df = pd.read_excel(file_path)
            else:
                raise ValueError(f"Unsupported file format {extension}. Please provide a CSV or Excel file.")
            
            logger.info(f"Dataset read successfully. Shape: {df.shape}")
            logger.info(f"Columns: {list(df.columns)}")
            
            return DataIngestionArtifact(
                dataframe=df,
                rows=df.shape[0],
                columns=df.shape[1],
                source_path=str(file_path)
            )
            
        except Exception as e:
            logger.error(f"Error occurred in data ingestion process.")
            raise CustomException(e, sys)
