from dataclasses import dataclass

@dataclass
class DataIngestionConfig:
    raw_data_path: str

@dataclass
class DataValidationConfig:
    validation_yaml_path: str

