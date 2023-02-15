
import time

from flask import Flask, render_template, make_response, request, Response, send_file

from pytube import YouTube
import youtube_dl

app = Flask(__name__)

# youtube
@app.route("/api/youtubedown", methods=["POST"])
def youtube_download():
    # Get the YouTube video link from the request parameters
    video_link = request.form.get("youtube_link")
    print(video_link)
    desired_quality = request.form.get("quality")
    print(desired_quality)
    print(video_link)
    filename = f"video_{int(time.time())}.mp4"
    # Check if the video link is provided
    if not video_link:
        return "Video link is not provided", 400

    # Download the video using the link
    try:
        yt = YouTube(video_link)
        if desired_quality=="highest_available":
            video = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first().download()
        else:
            video = yt.streams.filter(progressive=True, file_extension='mp4', resolution=desired_quality).first().download()
    except Exception as e:
        return f"Failed to download the video: {str(e)}", 400

    # Make the response object with the video as an attachment
    # with open(video, "rb") as f:
    #     response = Response(f.read(), content_type="video/mp4")
    #     response.headers["Content-Disposition"] = "inline; filename=video.mp4"
    headers = {
        'Content-Disposition': f'attachment; filename={filename}',
        'Content-Type': 'video/mp4'
    }
    return send_file(video,as_attachment=True,download_name=filename)
# .................................................
# facebook
@app.route("/api/facedown", methods=["POST"])
def facedown():
    video_link = request.form.get("facebook_link")
    if video_link is None:
        return "Please provide a Facebook video link", 400
    filename = f"video_{int(time.time())}.mp4"
    ydl_opts = {
        "outtmpl": filename + ".%(ext)s",
        "format": "best[height<=720]+bestAudio/best",
        "merge_output_format": "mp4"
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        vido=ydl.download([video_link])

    # video_file = filename + ".mp4"

    with open(vido, "rb") as video:
        response = Response(video.read(), content_type="video/mp4")
        response.headers["Content-Disposition"] = "attachment; filename=video.mp4"

    return response
# .................................................
# insta
@app.route("/api/instadown", methods=["POST"])
def download_instagram_video():
    return "Comming Soon"
# .............................................
@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/youdown", methods=["GET"])
def youdown():
    return render_template("youtubedown.html")

@app.route("/facedown", methods=["GET"])
def facebookdown():
    return render_template("facedown.html")

@app.route("/instadown", methods=["GET"])
def instagramdown():
    return render_template("instadown.html")

if __name__ == "__main__":
    app.run(debug=True)
