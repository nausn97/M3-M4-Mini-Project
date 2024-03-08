import sys
from pathlib import Path
import typing as Typing
import joblib
import pandas as pd
from sklearn.pipeline import Pipeline
from stroke_model import __version__ as version
from stroke_model.config.core import DATASET_DIR, TRAINED_MODEL_DIR, config

file = Path(__file__).resolve()
parent, root = file.parent, file.parents[1]
sys.path.append(str(root))


def _load_raw_dataset(*, file_name: str) -> pd.DataFrame:
    dataframe = pd.read_csv(Path(f"{DATASET_DIR} / {file_name}"))
    return dataframe


def _load_dataset(*, file_name: str) -> pd.DataFrame:
    dataframe = pd.read_csv(Path(f"{DATASET_DIR}/{file_name}"))
    dataframe = pre_pipeline_process(dataframe=dataframe)
    return dataframe


def _save_pipeline(*, pipeline_to_persist: Pipeline) -> None:
    save_file_name = f"{config.app_config.pipeline_save_file}{version}.pkl"
    save_path = TRAINED_MODEL_DIR / save_file_name
    remove_old_pipelines(files_to_keep=[save_file_name])
    joblib.dump(pipeline_to_persist, save_path)


def _load_pipeline(*, file_name: str) -> Pipeline:
    file_path = TRAINED_MODEL_DIR / file_name
    trained_model = joblib.load(file_path)
    return trained_model


def remove_old_pipelines(*, files_to_keep: Typing.List[str]) -> None:
    do_not_delete = files_to_keep + ["__init__.py"]
    for model_file in TRAINED_MODEL_DIR.iterdir():
        if model_file.name not in do_not_delete:
            model_file.unlink()


def pre_pipeline_process(*, dataframe: pd.DataFrame) -> pd.DataFrame:
    dataframe.drop(['id'], axis=1, inplace=True)
    dataframe.dropna(axis=0, inplace=True)
    return dataframe




