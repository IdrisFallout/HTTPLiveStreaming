import subprocess
from fastapi import FastAPI
from fastapi.responses import Response, HTMLResponse

app = FastAPI()
is_starting = True


@app.get('/hls')
def generate_hls():
    input_file = 'D:\Multimedia\Shrek 2 (2004) [1080p]\Shrek.2.2004.1080p.BluRay.x264.YIFY.mp4'
    output_path = 'output/output.m3u8'

    global is_starting

    if is_starting:
        # Generate HLS segments from the video using ffmpeg
        subprocess.call([
            'ffmpeg', '-i', input_file, '-codec', 'copy', '-map', '0', '-f', 'hls', '-hls_time', '10', '-hls_list_size',
            '0', f'{output_path}'
        ])
        is_starting = False

    content = prefix_ts_urls(f'{output_path}')

    return Response(content=content, media_type="application/vnd.apple.mpegurl")


def prefix_ts_urls(file_path):
    prefix = "http://127.0.0.1:8000/output/"
    with open(file_path, "r") as f:
        lines = f.readlines()
        for i, line in enumerate(lines):
            if line.endswith(".ts\n"):
                lines[i] = prefix + line
    output = "".join(lines)
    return output


@app.get('/output/{segment}')
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
