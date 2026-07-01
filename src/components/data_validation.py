import sys
import yaml
from pathlib import Path
import pandas as pd
from src.logger import logger
from src.exception import CustomException
from src.entity.config_entity import DataValidationConfig
from src.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact

class DataValidation:
    """
    DataValidation component validates the structural integrity of the ingested dataset.
    Rules are defined in validation.yaml.
    """
    def __init__(self, config: DataValidationConfig):
        self.config = config

    def read_validation_rules(self) -> dict:
        """Reads structural validation rules from yaml file"""
        try:
            with open(self.config.validation_yaml_path, 'r') as f:
                return yaml.safe_load(f)['validation']
        except Exception as e:
            raise CustomException(e, sys)

    def initiate_data_validation(self, ingestion_artifact: DataIngestionArtifact) -> DataValidationArtifact:
        """
        Validates the schema (columns, required IDs) and returns DataValidationArtifact.
        """
        logger.info("Starting structural data validation process.")
        try:
            df = ingestion_artifact.dataframe.copy()
            initial_rows = df.shape[0]
            
            rules = self.read_validation_rules()
            
            required_columns = rules.get('required_columns', [])
            missing_cols = [col for col in required_columns if col not in df.columns]
            if missing_cols:
                raise ValueError(f"Missing required columns in dataset: {missing_cols}")
            
            if rules.get('drop_missing_customer', False):
                df = df.dropna(subset=['Customer ID'])
                logger.info(f"Dropped rows with missing Customer ID (structural requirement). Current shape: {df.shape}")
                
            final_rows = df.shape[0]
            dropped_rows = initial_rows - final_rows
            
            logger.info(f"Data validation complete. Initial rows: {initial_rows}, Final rows: {final_rows}, Dropped: {dropped_rows}")
            
            return DataValidationArtifact(
                cleaned_dataframe=df,
                initial_rows=initial_rows,
                final_rows=final_rows,
                dropped_rows=dropped_rows
            )
            
        except Exception as e:
            logger.error("Error occurred in data validation process.")
            raise CustomException(e, sys)
