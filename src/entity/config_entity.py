from dataclasses import dataclass

@dataclass
class DataIngestionConfig:
    raw_data_path: str

@dataclass
class DataValidationConfig:
    validation_yaml_path: str


@dataclass
class DataCleaningConfig:
    business_rules_yaml_path: str

@dataclass
class CustomerAggregationConfig:
    pass


@dataclass
class FeatureEngineeringConfig:
    features_yaml_path: str

