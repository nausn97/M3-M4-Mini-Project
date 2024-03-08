import pandas as pd
from typing import Union
from stroke_model.config.core import config
from stroke_model import __version__ as version
from stroke_model.processing.validation import validate_inputs
from stroke_model.pipeline import pipeline

def make_prediction(*, input_data: Union[pd.DataFrame, dict]):
    validated_data, errors = validate_inputs(input_df=pd.DataFrame(input_data))
    validated_data = validated_data.reindex(columns=config.model_config.feature_names)
    results = {"prediction": None, "version": version, "errors": errors}

    if not errors:
        prediction = pipeline.predict
        results = {"prediction": prediction, "version": version, "errors": errors}

    return results


if __name__ == "__main__":
    data_in = {'gender': 'Male', 'age': 32, 'hypertension': 0, 'heart_disease': 1,
               'ever_married': 'Yes',
               'work_type': 'Private',
               'Residence_type': 'Rural',
               'avg_glucose_level': 232,
               'bmi': 27,
               'smoking_status': 'smokes' }


    make_prediction(input_data=data_in)