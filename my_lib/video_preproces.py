import av
import numpy as np
import base64
import io
from PIL import Image

def read_video_pyav(container, indices):
    frames = []
    container.seek(0)
    start_index, end_index = indices[0], indices[-1]

    for i, frame in enumerate(container.decode(video=0)):
        if i > end_index:
            break
        if i >= start_index and i in indices:
            frames.append(frame)

    return np.stack([x.to_ndarray(format="rgb24") for x in frames])

# def process_video(video_path, num_frames=4):
#     container = av.open(video_path)
#     total_frames = container.streams.video[0].frames
#     indices = np.arange(0, total_frames, total_frames / num_frames).astype(int)

#     clip = read_video_pyav(container, indices)

#     frame_bytes = io.BytesIO()
#     np.save(frame_bytes, clip, allow_pickle=False)
#     return base64.b64encode(frame_bytes.getvalue()).decode("utf-8")

def process_video(video_path, num_frames=4):
    container = av.open(video_path)
    total_frames = container.streams.video[0].frames

    # Fallback if total_frames is None or 0
    if not total_frames or total_frames == 0:
        total_frames = sum(1 for _ in container.decode(video=0))
        container = av.open(video_path)  # reset for actual frame reading

    if total_frames == 0:
        raise ValueError("Could not extract frames: total frame count is zero.")

    # Ensure num_frames doesn't exceed total
    num_frames = min(num_frames, total_frames)

    # Avoid division by zero in np.arange
    if num_frames <= 1:
        indices = np.array([0])
    else:
        indices = np.linspace(0, total_frames - 1, num_frames).astype(int)

    clip = read_video_pyav(container, indices)

    frame_bytes = io.BytesIO()
    np.save(frame_bytes, clip, allow_pickle=False)
    return base64.b64encode(frame_bytes.getvalue()).decode("utf-8")


def process_image_as_video(image_path, num_frames=2):
    image = Image.open(image_path).convert("RGB")
    image_array = np.array(image)
    video_frames = np.repeat(image_array[np.newaxis, ...], num_frames, axis=0)

    frame_bytes = io.BytesIO()
    np.save(frame_bytes, video_frames, allow_pickle=False)  # keep False if model expects that
    return base64.b64encode(frame_bytes.getvalue()).decode("utf-8")

