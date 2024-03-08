import sys
from pathlib import Path
file = Path(__file__).resolve()
parent, root = file.parent, file.parents[1]
sys.path.append(str(root))

from typing import List, Optional, Tuple, Union
from pydantic import BaseModel, Field, field_validator, ValidationError
import panda as pd
import numpy as np



def validate_inputs(*, input_df: pd.DataFrame) -> Tuple[pd.DataFrame, Optional[dict]]:
    validated_data = None
    errors = None
    try:
        MultipleDataInputs(
            inputs=validated_data.replace({np.nan: None}).to_dict(orient="records")
        )
    except ValidationError as error:
        errors = error.json()

    return validated_data, errors

class DataInputSchema(BaseModel):
    gender: str = Field(description="Gender of the person Male | Female")
    age: int = Field(gt=0, lt=100)
    hypertension: int = Field(gt=-1, lt=2, description="Value of Hypertension of the person should be 0 | 1")
    heart_disease: int = Field(gt=-1, lt=2, description="Value of Heart Disease of the person should be 0 | 1")
    ever_married: int = Field(gt=-1, lt=2, description="Value of Ever Married of the person should be 0 | 1")
    work_type: str
    residence_type: str
    avg_glucose_level: float = Field(gt=0, lt=300, description="Value of Glucose Level between 1 to 300")
    bmi: float = Field(gt=0, lt=30, description="Value of Glucose Level between 1 to 30")
    smoking_status: str

    @field_validator("gender")
    @classmethod
    def validate_gender(cls, v: str) -> str:
        if v not in ["Male", "Female"]:
            raise ValueError("Gender must be Male or Female")
        return v


    @field_validator("work_type")
    @classmethod
    def validate_work_type(cls, v: str) -> str:
        if v not in ["Private", "Self-employed", "children", "Govt_job", "Never_worked"]:
            raise ValueError("It must be in one among -> Private, Self-employed, children, Govt_job, Never_worked")
        return v


    @field_validator("smoking_status")
    @classmethod
    def validate_smoking_status(cls, v: str) -> str:
        if v not in ["formerly smoked", "never smoked", "smokes", "Unknown"]:
            raise ValueError("It must be in one among -> formerly smoked, never smoked, smokes, Unknown")
        return v


    @field_validator("residence_type")
    @classmethod
    def validate_residence_type(cls, v: str) -> str:
        if v not in ["Rural", "Urban"]:
            raise ValueError("It must be in one among -> Rural, Urban")
        return v


class MultipleDataInputs(BaseModel):
    inputs: List[DataInputSchema]