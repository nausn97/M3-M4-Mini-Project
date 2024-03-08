from fastapi import FastAPI, APIRouter, Depends, HTTPException, status
from starlette import status
from typing import Annotated
from auth.auth import get_current_user
from pydantic import BaseModel, Field, validator, field_validator

router = APIRouter()
user_dependency = Annotated[dict, Depends(get_current_user)]


class HealthData(BaseModel):
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


class ResponseModel(BaseModel):
    prediction: float
    probability: float


@router.post("/predict",
             status_code=status.HTTP_200_OK)
def predict_stroke(user: user_dependency,
                   health_data: HealthData):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication Failed")
    # data preprocessing
    # model.prediction
    # prepare a dictionary for response
    response = {'prediction': 94, 'probability': 94.7}
    return response
