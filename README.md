# Video Summarization

A Python-based service for automatic video and image summarization. This project extracts key frames from videos and leverages the Llava Next Video 7B HF model to generate meaningful summaries of the content. It also supports image summarization.

## Features

- **Video Summarization:**  
  Extracts key frames from uploaded videos and summarizes the video’s content using a state-of-the-art vision-language model.

- **Image Summarization:**  
  Summarizes the content of uploaded images.

- **REST API:**  
  Easy integration via HTTP POST requests for both video and image summarization.

## How It Works

1. **Video Processing:**  
   - Key frames are extracted from the input video.
   - The extracted frames are passed to the Llava Next Video 7B HF model.
   - The model generates a natural language summary of the video.

2. **Image Processing:**  
   - The image is sent directly to the model for summarization.

## Tech Stack

- **Python** (88.1%)
- **Makefile** (7.1%)
- **Dockerfile** (4.8%)
- **Llava Next Video 7B HF** (HuggingFace Vision-Language Model)
- **FastAPI** (or similar, assumed for REST API)
- **OpenCV** (assumed for key frame extraction)

## Installation

**1. Clone the repository:**
```bash
git clone https://github.com/Muhammadyousafrana/video_summarization.git
cd video_summarization
```

**2. (Optional) Set up a virtual environment:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**3. Install dependencies:**
```bash
pip install -r requirements.txt
```

**4. (Optional) Run with Docker:**
```bash
docker build -t video_summarization .
docker run -p 80:80 video_summarization
```

## Usage

### API Endpoints

#### 1. Video Summarization

```bash
curl -X 'POST' \
  'http://<host>:<port>/summarize/' \
  -H 'accept: application/json' \
  -H 'Content-Type: multipart/form-data' \
  -F 'file=@your_video.mp4;type=video/mp4' \
  -F 'is_image=false'
```

#### 2. Image Summarization

```bash
curl -X 'POST' \
  'http://<host>:<port>/summarize/' \
  -H 'accept: application/json' \
  -H 'Content-Type: multipart/form-data' \
  -F 'file=@your_image.png;type=image/png' \
  -F 'is_image=true'
```

- Replace `<host>:<port>` with your deployed server address (e.g., `localhost:80`).

### API Response

A successful response returns a JSON object containing a summary, e.g.:

```json
{
  "summary": "This video explains how logos can enhance your personal brand..."
}
```

## Example

#### Video Example
```bash
curl -X 'POST' \
  'https://urban-robot-wp5r679rgwvcrjv-80.app.github.dev/summarize/' \
  -H 'accept: application/json' \
  -H 'Content-Type: multipart/form-data' \
  -F 'file=@example_video.mp4;type=video/mp4' \
  -F 'is_image=false'
```

#### Image Example
```bash
curl -X 'POST' \
  'https://urban-robot-wp5r679rgwvcrjv-80.app.github.dev/summarize/' \
  -H 'accept: application/json' \
  -H 'Content-Type: multipart/form-data' \
  -F 'file=@example_image.png;type=image/png' \
  -F 'is_image=true'
```

## Configuration

- **Model:** Llava Next Video 7B HF (ensure access to the HuggingFace model)
- **Environment variables:**  
  - See `.env.example` (if provided)
- **Key frame extraction:** Adjust extraction parameters in the config or code as needed.

## Requirements

- Python 3.8+
- See `requirements.txt` for full Python dependencies
- Docker (optional, for containerized deployment)

## Contributing

1. Fork the repository.
2. Create your feature branch: `git checkout -b feature/your-feature`
3. Commit your changes: `git commit -am 'Add new feature'`
4. Push to the branch: `git push origin feature/your-feature`
5. Open a pull request.

## License

[MIT License](LICENSE) (or specify your license)

## Contact

- Author: Muhammadyousafrana
- GitHub: [Muhammadyousafrana](https://github.com/Muhammadyousafrana)
