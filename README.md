# Media Summarizer API

A FastAPI service for summarizing uploaded videos and images using a vision-language model deployed through AWS SageMaker.

This project is designed for multimodal summarization: it extracts key frames from videos and sends them, along with a prompt, to the LLaVA-NeXT-Video model for summary generation. It also supports image summarization.

## Recommended repository name

The current repo name, `video_summarization`, works, but it is a little narrow because the application also supports image summarization.

A more appropriate and professional name would be:

- `media-summarizer-api`

Other good alternatives:
- `video-image-summarizer`
- `multimodal-summarizer-api`
- `video-summarizer-service`

## Features

- Summarize uploaded videos
- Summarize uploaded images
- REST API for integration with web or mobile apps
- Uses key-frame extraction for efficient video processing
- Runs with FastAPI and AWS SageMaker inference

## Tech stack

- Python
- FastAPI
- OpenCV / PyAV for video frame extraction
- Hugging Face LLaVA-NeXT-Video-7B
- AWS SageMaker Runtime
- Docker

## Project structure

```text
.
├── main.py
├── my_lib/
│   └── video_preproces.py
├── requirements.txt
├── Dockerfile
├── heroku.yml
├── Makefile
├── buildspec.yml
├── README.md
├── LICENSE
├── .gitignore
└── .dockerignore
```

## Installation

1. Clone the repository:

```bash
git clone https://github.com/Muhammadyousafrana/video_summarization.git
cd video_summarization
```

2. Create a virtual environment (optional but recommended):

```bash
python3 -m venv venv
source venv/bin/activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Set required environment variables for AWS SageMaker:

```bash
export aws_access_key_id="your_key"
export aws_secret_access_key="your_secret"
export endpoint="your_sagemaker_endpoint_name"
```

5. Run the app:

```bash
uvicorn main:app --reload
```

## API usage

### Summarize a video or image

Send a multipart form request to `/summarize` with:
- `file`: uploaded video or image
- `content-type`: automatically detected from the uploaded file

#### Example for video

```bash
curl -X POST "http://localhost:8000/summarize" \
  -H "accept: application/json" \
  -F "file=@example_video.mp4;type=video/mp4"
```

#### Example for image

```bash
curl -X POST "http://localhost:8000/summarize" \
  -H "accept: application/json" \
  -F "file=@example_image.png;type=image/png"
```

### Response format

```json
{
  "summary": "This video explains..."
}
```

## How it works

1. The uploaded file is checked to see whether it is a video or image.
2. For video input, key frames are extracted.
3. Frames are converted into a model-compatible format.
4. The LLaVA-NeXT-Video model generates a summary.
5. The summary is returned as a JSON response.

## Notes

- This project is more of a functional prototype/demo than a fully production-hardened service.
- AWS credentials should ideally be managed using IAM roles or a secure environment secret manager.
- Model and deployment configuration should be validated for production use.

## License

This project is licensed under the MIT License.

## Author

Muhammadyousafrana
