from fastapi import FastAPI, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
from process_photos import process_folder
from settings_util import load_settings



app = FastAPI()

# Allow CORS for local Next.js frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# Request model for pipeline trigger
class PipelineRequest(BaseModel):
    input: str = None
    output: str = None
    duplicates: str = None

@app.post("/run-pipeline/")
def run_pipeline(request: PipelineRequest, background_tasks: BackgroundTasks):
    # Use request, settings.json, or env vars (in that order)
    settings = load_settings()
    input_folder = request.input or settings.get("input") or os.environ.get("PHOTO_INPUT_FOLDER")
    output_folder = request.output or settings.get("output") or os.environ.get("PHOTO_OUTPUT_FOLDER", "./organized_photos")
    duplicates_folder = request.duplicates or settings.get("duplicates") or os.environ.get("PHOTO_DUPLICATE_FOLDER", "./duplicates")
    if not input_folder:
        return {"status": "error", "message": "Input folder not specified"}
    background_tasks.add_task(process_folder, input_folder, output_base=output_folder, duplicate_folder=duplicates_folder)
    return {"status": "started", "input": input_folder, "output": output_folder, "duplicates": duplicates_folder}

@app.get("/healthz")
def healthz():
    return {"status": "ok"}
