# video_summarization

### curl it
```sh
curl -X 'POST' \
  'https://urban-robot-wp5r679rgwvcrjv-80.app.github.dev/summarize/' \
  -H 'accept: application/json' \
  -H 'Content-Type: multipart/form-data' \
  -F 'file=@4, How Logos Can Enhance Your Personal Brand - Zero To Mastery Academy - 1920x1080 259K.mp4;type=video/mp4' \
  -F 'is_image=false'
```

```sh
curl -X 'POST' \
  'https://urban-robot-wp5r679rgwvcrjv-80.app.github.dev/summarize/' \
  -H 'accept: application/json' \
  -H 'Content-Type: multipart/form-data' \
  -F 'file=@6-step-ml-framework.png;type=image/png' \
  -F 'is_image=true'
```