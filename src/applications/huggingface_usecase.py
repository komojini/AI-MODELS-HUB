from .base import UseCase
from huggingface_hub import HfApi
from huggingface_hub.hf_api import ModelInfo
import dataclasses


class HuggingFaceListModelsUseCase(UseCase):
    def __init__(self, api: HfApi):
        self.api = api
    
    def execute(self, *args, **kwargs) -> list[ModelInfo]:
        return self.api.list_models(*args, **kwargs)


class HuggingFaceListModelJsonUseCase(UseCase):
    def __init__(self, api: HfApi):
        self.api = api
    
    def execute(self, *args, **kwargs) -> list[dict]:
        models =  self.api.list_models(*args, **kwargs)
        return [model.__dict__ for model in models]