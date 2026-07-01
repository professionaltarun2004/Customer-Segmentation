import sys
import yaml
import importlib
import pandas as pd
from src.logger import logger
from src.exception import CustomException
from src.entity.config_entity import FeatureEngineeringConfig
from src.entity.artifact_entity import CustomerAggregationArtifact, FeatureEngineeringArtifact, DataCleaningArtifact
from src.components.features.base import BaseFeatureBuilder

class FeatureEngineering:
    """
    Orchestrator for the Feature Engineering framework.
    Dynamically loads feature builders defined in configs/features.yaml
    and applies them sequentially.
    """
    def __init__(self, config: FeatureEngineeringConfig):
        self.config = config
        self.builders = []

    def _load_builders(self):
        """Reads configuration and instantiates the enabled feature builders."""
        try:
            with open(self.config.features_yaml_path, 'r') as f:
                enabled_features = yaml.safe_load(f).get('enabled_features', [])
                
            for feature_name in enabled_features:
                # Assuming modules are named exactly as in the yaml (e.g. 'value')
                # and classes are named CamelCase (e.g. 'ValueFeatureBuilder')
                module_name = f"src.components.features.{feature_name}"
                class_name = feature_name.replace("_", " ").title().replace(" ", "") + "FeatureBuilder"
                
                module = importlib.import_module(module_name)
                builder_class = getattr(module, class_name)
                
                self.builders.append(builder_class())
                logger.info(f"Registered FeatureBuilder: {class_name}")
                
        except Exception as e:
            logger.error("Failed to load feature builders.")
            raise CustomException(e, sys)

    def initiate_feature_engineering(self, 
                                     aggregation_artifact: CustomerAggregationArtifact,
                                     cleaning_artifact: DataCleaningArtifact = None) -> FeatureEngineeringArtifact:
        """
        Executes all registered feature builders in sequence.
        """
        logger.info("Starting orchestrated feature engineering process.")
        try:
            self._load_builders()
            
            df = aggregation_artifact.aggregated_dataframe.copy()
            df_raw = cleaning_artifact.cleaned_dataframe if cleaning_artifact else None
            
            feature_artifacts = []
            
            for builder in self.builders:
                logger.info(f"Applying builder: {builder.__class__.__name__}")
                df, artifact = builder.transform(df, df_raw)
                feature_artifacts.append(artifact)
                logger.info(f"Generated features: {artifact.features_created} in {artifact.execution_time_ms:.2f}ms")
            
            logger.info(f"Feature engineering complete. Final shape: {df.shape}")
            
            return FeatureEngineeringArtifact(
                feature_dataframe=df,
                feature_artifacts=feature_artifacts
            )
            
        except Exception as e:
            logger.error("Error occurred during feature engineering orchestration.")
            raise CustomException(e, sys)
