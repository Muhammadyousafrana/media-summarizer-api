from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import JSONResponse
import gzip
import json
import boto3
import tempfile
from transformers import LlavaNextVideoProcessor
from my_lib.video_preproces import process_video, process_image_as_video

app = FastAPI()

# Load once
processor = LlavaNextVideoProcessor.from_pretrained("llava-hf/LLaVA-NeXT-Video-7B-hf")
runtime = boto3.client("sagemaker-runtime")
ENDPOINT_NAME = "huggingface-pytorch-inference-2025-03-02-14-00-37-715"

@app.post("/summarize/")
async def summarize_media(
    file: UploadFile = File(...),
    prompt_text: str = Form(...),
    is_image: bool = Form(False),
    num_frames: int = Form(8)
):
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=file.filename) as tmp:
            tmp.write(await file.read())
            tmp_path = tmp.name

        if is_image:
            compressed_frames = process_image_as_video(tmp_path, num_frames)
        else:
            compressed_frames = process_video(tmp_path, num_frames)

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
            "video_frames": compressed_frames,
            "max_new_tokens": 512
        }

        compressed_payload = gzip.compress(json.dumps(payload).encode("utf-8"))

        response = runtime.invoke_endpoint(
            EndpointName="huggingface-pytorch-inference-2025-04-11-13-13-58-931",
            ContentType="application/gzip",
            Body=compressed_payload,
        )

        result = response["Body"].read().decode("utf-8")
        return JSONResponse(content={"summary": result})
    
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
