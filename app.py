from flask import Flask, render_template, request, send_file
import yt_dlp
import os
import uuid

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        url = request.form.get("url")
        if not url:
            return render_template("index.html", error="Vui lòng nhập link YouTube!")

        try:
            os.makedirs("downloads", exist_ok=True)
            output_path = f"downloads/{uuid.uuid4()}.mp4"

            ydl_opts = {
                "format": "best",
                "outtmpl": output_path,
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])

            return send_file(output_path, as_attachment=True)

        except Exception as e:
            return render_template("index.html", error=f"Lỗi khi tải: {str(e)}")

    return render_template("index.html")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
