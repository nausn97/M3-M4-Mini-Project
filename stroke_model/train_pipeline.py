import sys
from pathlib import Path
file = Path(__file__).resolve()
parent, root = file.parent, file.parents[1]
sys.path.append(str(root))

from sklearn.model_selection import train_test_split
from stroke_model.processing.data_manager import _load_dataset
from stroke_model.config.core import config
from stroke_model.pipeline import Pipeline
from stroke_model.processing.data_manager import _save_pipeline


def train_pipeline() -> None:
    data = _load_dataset(file_name=config.app_config.training_data_file)
    X_train, X_test, y_train, y_test = train_test_split(
        data[['gender', 'age', 'hypertension', 'heart_disease', 'ever_married', 'work_type', 'Residence_type', 'avg_glucose_level', 'bmi', 'smoking_status']],
        data['stroke'],
        # test_size=config.model_config.test_size,
        test_size=0.2,
        random_state=42
    )
    Pipeline.fit(X_train, y_train)
    _save_pipeline(pipeline_to_persist=Pipeline)


if __name__ == "__main__":
    train_pipeline()

