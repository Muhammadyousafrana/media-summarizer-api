from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
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
    aws_access_key_id="AKIAUUJ3ZEYEARBUC7K6",
    aws_secret_access_key="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"
)

# Load processor once
processor = LlavaNextVideoProcessor.from_pretrained("llava-hf/LLaVA-NeXT-Video-7B-hf")
ENDPOINT_NAME = "huggingface-pytorch-inference-2025-04-17-14-30-52-638"


@app.get("/")
async def root():
    return {"message": "Welcome to the Summarization API. Use /summarize to summarize media files."}


@app.post("/summarize/")
async def summarize_media(file: UploadFile = File(...)):
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=file.filename) as tmp:
            tmp.write(await file.read())
            tmp_path = tmp.name

        # Detect MIME type
        if file.content_type.startswith("image/"):
            compressed_frames = process_image_as_video(tmp_path)
        elif file.content_type.startswith("video/"):
            compressed_frames = process_video(tmp_path)
        else:
            return JSONResponse(
                status_code=400,
                content={"error": f"Unsupported file type: {file.content_type}"}
            )

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
            "max_new_tokens": 1024
        }

        compressed_payload = gzip.compress(json.dumps(payload).encode("utf-8"))

        response = runtime.invoke_endpoint(
            EndpointName=ENDPOINT_NAME,
            ContentType="application/gzip",
            Body=compressed_payload,
        )

        result = response["Body"].read().decode("utf-8")
        return JSONResponse(content={"summary": result[0][2:]})

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
