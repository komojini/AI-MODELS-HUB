from fastapi import FastAPI
import os
from pathlib import Path
import logging
import json
from typing import List
from datetime import datetime

from src.applications.huggingface_usecase import HuggingFaceListModelJsonUseCase
from src.adapters.api.huggingface_api import HuggingFaceAPI

app = FastAPI()
logging.basicConfig(level=logging.INFO)
logging.info("Starting FastAPI app")


huggingface_use_case = HuggingFaceListModelJsonUseCase(api=HuggingFaceAPI())

def get_root_dir(curr_dir: Path = None, max_depth: int = 5, depth: int = 0) -> Path:
    if curr_dir is None:
        curr_dir = Path(os.path.abspath(__file__))
    if curr_dir.name == "src":
        logging.info(f"Found root directory: {curr_dir.parent.absolute()}")
        return curr_dir.parent
    else:
        if depth < max_depth:
            return get_root_dir(curr_dir.parent, depth=depth+1)
        else:
            raise Exception(f"Could not find root directory, current directory: {curr_dir.absolute()}")


def get_cache_dir() -> Path:
    return get_root_dir() / ".cache"


def cache_data(data: dict, cache_dir: Path, filename: str):
    logging.info(f"Caching data to {cache_dir.absolute()} with filename {filename}, data.type: {type(data)}")
                 
    if not cache_dir.exists():
        cache_dir.mkdir(parents=True)
    with open(cache_dir / filename, "w") as f:
        json.dump(data, f)

def get_now_str() -> str:
    now = datetime.now()
    return now.strftime('%Y%m%d%H%M%S')


@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.get("/models/{model_id}")
async def read_model(model_id: int):
    return {"model_id": model_id, "model_name": "alexnet"}


@app.get("/models/")
async def read_models(
        author: str | None = None,
        limit: int | None = None,
    ):
    logging.info("Getting models from HuggingFace Hub")

    return huggingface_use_case.execute(
        author=author,
        limit=limit,
    )


@app.get("/cache_models/")
async def cache_models(
        author: str | None = None,
        limit: int | None = None, 
    ):
    logging.info("Caching models from HuggingFace Hub")
    models = huggingface_use_case.execute(
        author=author,
        limit=limit,
    )
    cache_data(models, get_cache_dir() / "huggingface_hub", f"models_{get_now_str()}.json")
    return models