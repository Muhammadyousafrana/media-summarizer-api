import os
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
from fastapi.logger import logger
import traceback
import base64
import gzip
import json
import boto3
import tempfile
from transformers import LlavaNextVideoProcessor
from my_lib.video_preproces import read_video_pyav, process_video, process_image_as_video

app = FastAPI()

# Explicit AWS credentials (consider moving to env vars or IAM roles in production)
runtime = boto3.client(
    "sagemaker-runtime",
    region_name="us-east-1",
    aws_access_key_id=os.getenv("aws_access_key_id"),
    aws_secret_access_key=os.getenv("aws_secret_access_key")
)

# Load processor once
processor = LlavaNextVideoProcessor.from_pretrained("llava-hf/LLaVA-NeXT-Video-7B-hf")
ENDPOINT_NAME = os.getenv("endpoint")


@app.get("/")
async def root():
    return {"message": "Welcome to the Summarization API. Use /summarize to summarize media files."}


@app.post("/summarize")
async def summarize_media(file: UploadFile = File(...)):
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=file.filename) as tmp:
            tmp.write(await file.read())
            tmp_path = tmp.name

        logger.info(f"Received file: {file.filename}, content type: {file.content_type}")

        is_video = file.content_type.startswith("video/")
        is_image = file.content_type.startswith("image/")

        if not (is_video or is_image):
            return JSONResponse(
                status_code=400,
                content={"error": f"Unsupported file type: {file.content_type}"}
            )

        if is_video:
            try:
                compressed_frames = process_video(tmp_path)
                prompt_text = "summarize this video and explain the key highlights"
            except Exception as ve:
                logger.error(f"Error processing video: {ve}")
                logger.debug(traceback.format_exc())
                return JSONResponse(
                    status_code=400,
                    content={"error": f"Video processing failed: {str(ve)}"}
                )
        else:  # is_image
            try:
                compressed_frames = process_image_as_video(tmp_path)
                prompt_text = "describe the image and summarize its content"
            except Exception as ie:
                logger.error(f"Error processing image: {ie}")
                logger.debug(traceback.format_exc())
                return JSONResponse(
                    status_code=400,
                    content={"error": f"Image processing failed: {str(ie)}"}
                )

        conversation = [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt_text},
                    {"type": "video"},
                ],
            },
        ]

        prompt = processor.apply_chat_template(conversation, add_generation_prompt=True)

        payload = {
            "prompt": prompt,
            "video_frames": compressed_frames,  # still using "video_frames" key for SageMaker input
            "max_new_tokens": 1024
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
        logger.error(f"Unhandled error: {e}")
        logger.debug(traceback.format_exc())
        return JSONResponse(status_code=500, content={"error": str(e)})
