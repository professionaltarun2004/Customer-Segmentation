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
    DataValidation component applies business-defined rules to clean
    the ingested dataset. Rules are defined in validation.yaml.
    """
    def __init__(self, config: DataValidationConfig):
        self.config = config

    def read_validation_rules(self) -> dict:
        """Reads validation rules from yaml file"""
        try:
            with open(self.config.validation_yaml_path, 'r') as f:
                return yaml.safe_load(f)['validation']
        except Exception as e:
            raise CustomException(e, sys)

    def initiate_data_validation(self, ingestion_artifact: DataIngestionArtifact) -> DataValidationArtifact:
        """
        Applies validation rules on the dataset and returns DataValidationArtifact.
        """
        logger.info("Starting data validation process.")
        try:
            df = ingestion_artifact.dataframe.copy()
            initial_rows = df.shape[0]
            
            rules = self.read_validation_rules()
            
            if rules.get('drop_missing_customer', False):
                df = df.dropna(subset=['Customer ID'])
                logger.info(f"Dropped missing customers. Current shape: {df.shape}")
                
            if rules.get('drop_missing_invoicedate', False):
                if 'InvoiceDate' in df.columns:
                    df = df.dropna(subset=['InvoiceDate'])
                    logger.info(f"Dropped missing invoice dates. Current shape: {df.shape}")
            
            if rules.get('remove_cancelled_invoice', False):
                df = df[~df['Invoice'].astype(str).str.startswith('C', na=False)]
                logger.info(f"Removed cancelled invoices. Current shape: {df.shape}")
                
            if rules.get('remove_negative_quantity', False):
                df = df[df['Quantity'] > 0]
                logger.info(f"Removed negative quantity rows. Current shape: {df.shape}")
                
            if rules.get('remove_negative_price', False):
                df = df[df['Price'] >= 0]  # price can technically be zero, though negative is bad
                logger.info(f"Removed negative price rows. Current shape: {df.shape}")
                
            if rules.get('remove_duplicates', False):
                df = df.drop_duplicates()
                logger.info(f"Removed duplicates. Current shape: {df.shape}")
                
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
