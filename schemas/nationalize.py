from pydantic import BaseModel, ConfigDict, EmailStr, Field, model_validator


class InputName(BaseModel):
    name: str = "johnson"


class CountryPrediction(BaseModel):
    country: str
    country_code: str
    probability: float


class NamePredictionResponse(BaseModel):
    name: str
    results: list[CountryPrediction]


class TopNameStat(BaseModel):
    name: str
    probability: float


class PopularNamesResponse(BaseModel):
    country: str
    top_names: list[TopNameStat]
