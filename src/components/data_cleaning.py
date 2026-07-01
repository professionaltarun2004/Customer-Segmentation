import sys
import yaml
from pathlib import Path
import pandas as pd
from src.logger import logger
from src.exception import CustomException
from src.entity.config_entity import DataCleaningConfig
from src.entity.artifact_entity import DataValidationArtifact, DataCleaningArtifact

class DataCleaning:
    """
    DataCleaning component applies business-defined rules to filter and clean
    the structurally validated dataset. Rules are defined in business_rules.yaml.
    """
    def __init__(self, config: DataCleaningConfig):
        self.config = config

    def read_business_rules(self) -> dict:
        """Reads business cleaning rules from yaml file"""
        try:
            with open(self.config.business_rules_yaml_path, 'r') as f:
                return yaml.safe_load(f)['business_rules']
        except Exception as e:
            raise CustomException(e, sys)

    def initiate_data_cleaning(self, validation_artifact: DataValidationArtifact) -> DataCleaningArtifact:
        """
        Applies business cleaning logic and returns DataCleaningArtifact.
        """
        logger.info("Starting business data cleaning process.")
        try:
            df = validation_artifact.cleaned_dataframe.copy()
            initial_rows = df.shape[0]
            
            rules = self.read_business_rules()
            
            # Example business rule: removing cancelled invoices
            if rules.get('remove_cancelled_invoice', False):
                df = df[~df['Invoice'].astype(str).str.startswith('C', na=False)]
                logger.info(f"Removed cancelled invoices based on business rule. Current shape: {df.shape}")
            
            # Example business rule: handling returns (negative quantity)
            if not rules.get('keep_returns', True):
                df = df[df['Quantity'] > 0]
                logger.info(f"Removed return records (negative quantity) based on business rule. Current shape: {df.shape}")
                
            # Drop duplicates
            df = df.drop_duplicates()
            logger.info(f"Removed duplicates. Current shape: {df.shape}")
                
            final_rows = df.shape[0]
            dropped_rows = initial_rows - final_rows
            
            logger.info(f"Data cleaning complete. Initial rows: {initial_rows}, Final rows: {final_rows}, Dropped: {dropped_rows}")
            
            return DataCleaningArtifact(
                cleaned_dataframe=df,
                initial_rows=initial_rows,
                final_rows=final_rows,
                dropped_rows=dropped_rows
            )
            
        except Exception as e:
            logger.error("Error occurred in data cleaning process.")
            raise CustomException(e, sys)
