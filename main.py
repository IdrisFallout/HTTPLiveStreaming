from typing import List
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import Response, HTMLResponse
from pydantic import BaseModel
import subprocess

app = FastAPI()


class Video(BaseModel):
    file: UploadFile


@app.get('/hls')
def generate_hls():
    input_file = 'E:/Videos/MetraverseClass.mp4'
    output_path = 'output/'

    # Generate HLS segments from the video using ffmpeg
    # subprocess.call([
    #     'ffmpeg', '-i', input_file, '-codec', 'copy', '-map', '0', '-f', 'hls', '-hls_time', '10', '-hls_list_size',
    #     '0', f'{output_path}output.m3u8'
    # ])

    # Define the MIME type for HLS content
    headers = {
        'Content-Type': 'application/x-mpegURL'
    }

    # Open the output file and return the HLS stream
    with open(f'{output_path}output.m3u8', 'rb') as f:
        content = f.read()
    return Response(content=content, media_type="application/vnd.apple.mpegurl")


@app.get('/hls/{segment}')
async def hls(segment: str):
    with open(f'output/{segment}', 'rb') as f:
        content = f.read()
    return Response(content=content, media_type="video/MP2T")


# Serve the HTML file for playing the HLS content
@app.get("/")
async def get_index():
    with open("index.html", "r") as f:
        html_content = f.read()
    return HTMLResponse(content=html_content, status_code=200)