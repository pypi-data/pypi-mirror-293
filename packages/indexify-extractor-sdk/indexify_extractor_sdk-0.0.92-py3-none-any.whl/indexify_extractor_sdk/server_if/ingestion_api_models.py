import json
from typing import Any, Dict, List

from indexify.extractor_sdk import Content, Feature
from pydantic import BaseModel, Json


class ApiFeature(BaseModel):
    feature_type: str
    name: str
    data: Json

    @classmethod
    def from_feature(cls, feature: Feature):
        return cls(
            feature_type=feature.feature_type,
            name=feature.name,
            data=json.dumps(feature.value),
        )


class ApiContent(BaseModel):
    content_type: str
    bytes: List[int]
    features: List[ApiFeature] = []
    labels: Dict[str, Any] = {}

    @classmethod
    def from_content(cls, content: Content):
        content_features = []
        for feature in content.features:
            content_features.append(ApiFeature.from_feature(feature=feature))
        return cls(
            content_type=content.content_type,
            bytes=list(content.data),
            features=content_features,
            labels={},
        )


class BeginExtractedContentIngest(BaseModel):
    task_id: str
    executor_id: str
    task_outcome: str


class ExtractedFeatures(BaseModel):
    content_id: str
    features: List[ApiFeature]


class FinishExtractedContentIngest(BaseModel):
    num_extracted_content: int


class BeginMultipartContent(BaseModel):
    id: int


class ApiBeginExtractedContentIngest(BaseModel):
    BeginExtractedContentIngest: BeginExtractedContentIngest


class ApiFinishExtractedContentIngest(BaseModel):
    FinishExtractedContentIngest: FinishExtractedContentIngest


class ApiExtractedFeatures(BaseModel):
    ExtractedFeatures: ExtractedFeatures


class BeginMultipartContent(BaseModel):
    id: int


class ApiBeginMultipartContent(BaseModel):
    BeginMultipartContent: BeginMultipartContent


class FinishMultipartContent(BaseModel):
    content_type: str
    features: List[ApiFeature] = []
    labels: Dict[str, Any] = {}


class ApiFinishMultipartContent(BaseModel):
    FinishMultipartContent: FinishMultipartContent


class MultipartContentFrame(BaseModel):
    bytes: List[int]


class ApiMultipartContentFrame(BaseModel):
    MultipartContentFrame: MultipartContentFrame


class MultipartContentFeature(BaseModel):
    name: str
    values: List[float]


class ApiMultipartContentFeature(BaseModel):
    MultipartContentFeature: MultipartContentFeature
