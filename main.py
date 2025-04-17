from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import JSONResponse
import gzip
import json
import boto3
import tempfile
import base64
import io
import numpy as np
from PIL import Image
from transformers import LlavaNextVideoProcessor
from my_lib.video_preproces import read_video_pyav, process_video, process_image_as_video

app = FastAPI()

# Use explicit credentials here
runtime = boto3.client(
    "sagemaker-runtime",
    region_name="us-east-1",  # Your region
    aws_access_key_id="AKIAUUJ3ZEYEARBUC7K6",  # Replace with your access key
    aws_secret_access_key="BNxk6vbLhroI5igwSljr1sdYOs2gNjhh79aOZqEv"  # Replace with your secret key
)

# Load once
processor = LlavaNextVideoProcessor.from_pretrained("llava-hf/LLaVA-NeXT-Video-7B-hf")
ENDPOINT_NAME = "huggingface-pytorch-inference-2025-04-16-08-09-32-393"



@app.get("/")
async def root():
    return {"message": "Welcome to the Summarization API. Use /summarize/text to summarize text. and use /summarize/file to summarize the file"}


@app.post("/summarize/")
async def summarize_media(
    file: UploadFile = File(...),
    is_image: bool = Form(False)
):
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=file.filename) as tmp:
            tmp.write(await file.read())
            tmp_path = tmp.name

        if is_image:
            compressed_frames = process_image_as_video(tmp_path)
        else:
            compressed_frames = process_video(tmp_path)

        conversation = [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "summarize this video and explain the key highlight"},
                    {"type": "video"},
                ],
            },
        ]

        prompt = processor.apply_chat_template(conversation, add_generation_prompt=True)

        payload = {
            "prompt": prompt,
            "video_frames": compressed_frames,
            "max_new_tokens": 512
        }

        compressed_payload = gzip.compress(json.dumps(payload).encode("utf-8"))

        response = runtime.invoke_endpoint(
            EndpointName=ENDPOINT_NAME,
            ContentType="application/gzip",
            Body=compressed_payload,
        )

        result = response["Body"].read().decode("utf-8")
        return JSONResponse(content={"summary": result})
    
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
