from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Union


# Existing models from ProductCodeResponse
class Nutrient(BaseModel):
    name: str
    unit: str
    shortName: str
    group: Optional[str] = None
    origin: Optional[List[Dict[str, str]]] = None


class NutrientInfo(BaseModel):
    id: Optional[int] = None
    nutrient: Nutrient
    amount: float


class Weight(BaseModel):
    unit: str
    value: float


class Portion(BaseModel):
    weight: Weight
    name: str
    quantity: float
    suggestedQuantity: Optional[List[float]] = None


class Image(BaseModel):
    bucket: str
    path: str


class Branded(BaseModel):
    owner: Optional[str] = None
    productCode: Optional[str] = None
    ingredients: Optional[str] = None
    country: Optional[str] = None
    certified: Optional[bool] = None
    images: Optional[List[Image]] = None
    ocrText: Optional[str] = None
    reviewed: Optional[bool] = None
    tested: Optional[bool] = None
    upc: Optional[str] = None


class Origin(BaseModel):
    source: str
    id: str
    dataType: Optional[str] = None
    timestamp: str


# Base model for common fields
class BaseProductInfo(BaseModel):
    id: Optional[str] = None
    name: str
    nutrients: Optional[List[NutrientInfo]] = None
    portions: List[Portion]
    branded: Optional[Branded] = None
    origin: Optional[List[Origin]] = None
    qualityScore: Optional[str] = None
    timestamp: Optional[str] = None
    tags: Optional[List[str]] = None
    refCode: Optional[str] = None
    brandName: Optional[str] = None
    description: Optional[str] = None
    iconId: Optional[str] = None
    licenseCopy: Optional[str] = None
    name_i18n: Optional[Dict[str, str]] = None
    webLinks: Optional[List[str]] = None


# ProductCodeResponse (previously APIResponse)
class ProductCodeResponse(BaseProductInfo):
    pass


class Alternative(BaseModel):
    displayName: str
    iconId: Optional[str] = None
    labelId: Optional[str] = None
    resultId: Optional[str] = None
    type: Optional[str] = None


class SearchResult(BaseModel):
    displayName: str
    iconId: Optional[str] = None
    type: str
    refCode: str
    # Optional fields
    ingredients: Optional[List[Dict]] = None
    internalId: Optional[str] = None
    internalName: Optional[str] = None
    portions: Optional[List[Dict]] = None


class SearchResponse(BaseModel):
    results: List[SearchResult]
    alternatives: Optional[List[Alternative]] = None
