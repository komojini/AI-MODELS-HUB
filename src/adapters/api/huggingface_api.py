from huggingface_hub import HfApi

from .base import AIModelAPI


class HuggingFaceAPI(HfApi, AIModelAPI):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    