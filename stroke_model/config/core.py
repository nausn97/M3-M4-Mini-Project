import sys
import stroke_model
from typing import Dict, List
from pydantic import BaseModel
from strictyaml import YAML, load
from pathlib import Path


file = Path(__file__).resolve()
parent, root = file.parent, file.parents[1]
sys.path.append(str(root))


PACKAGE_ROOT = Path(stroke_model.__file__).resolve().parent
print(f"path of package root {PACKAGE_ROOT}")
ROOT = PACKAGE_ROOT.parent


CONFIG_FILE_PATH = PACKAGE_ROOT / 'config.yml'
print(PACKAGE_ROOT)
DATASET_DIR = PACKAGE_ROOT / 'datasets'
TRAINED_MODEL_DIR = PACKAGE_ROOT / 'trained_model'


class AppConfig(BaseModel):
    package_name: str
    training_data_file: str
    test_data_file: str
    pipeline_save_file: str


class ModelConfig(BaseModel):
    target: str
    features: List[str]
    unused_features: List[str]
    categorical_features: List[str]
    numerical_features: List[str]
    test_size: float
    random_state: int
    cv: int
    n_estimators: int
    max_depth: int


class Config(BaseModel):
    app_config: AppConfig
    model_config: ModelConfig


def get_config_file_path() -> Path:
    if CONFIG_FILE_PATH.is_file():
        return CONFIG_FILE_PATH
    raise Exception(f"Config file not found: {CONFIG_FILE_PATH}")


def get_config_from_yaml(config_file_path: Path = None) -> YAML:
    if not config_file_path:
        config_file_path = get_config_file_path()
    if config_file_path:
        with open(config_file_path, "r") as config_file:
            parsed_config = load(config_file.read())
            return parsed_config
    raise OSError(f"Config file not found: {config_file_path}")


def create_validated_config(parsed_config: YAML = None) -> Config:
    if parsed_config is None:
        parsed_config = get_config_from_yaml()
    _config = Config(
        app_config=AppConfig(**parsed_config.data),
        model_config=ModelConfig(**parsed_config.data)
    )
    return _config


config = create_validated_config()
