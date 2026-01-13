from flask import (
    Flask,
    jsonify,
    make_response,
    redirect,
    render_template,
    request,
    send_file,
    url_for,
)
from werkzeug.utils import secure_filename
from flaskwebgui import FlaskUI
import sys

sys.path.append("../../")
from lib import ImageGafter
from os.path import exists

app = Flask(__name__)


API_KEY_FILE = "./lib/config.json"

image_file_path = ""
n_images = 1


@app.get("/<name>")
def set_icon(name):
    if name == "favicon.ico":
        return send_file("static./images/logo.ico", mimetype="image/x-icon")


@app.route("/", methods=["GET", "OPTIONS"])
def index():
    if request.method == "OPTIONS":  # CORS preflight
        return _build_cors_preflight_response()
    else:
        return render_template("index.html")


@app.route("/get_prompts", methods=["GET", "OPTIONS"])
def get_prompts():
    if request.method == "OPTIONS":
        return _build_cors_preflight_response()
    else:
        prompts = ImageGafter.get_text_prompts(image_file_path, n_images)
        print(prompts)
        images = ImageGafter.generate_images(prompts, "outputs", API_KEY_FILE)
        # img_file_des = "The image captures a formal event, possibly an awards ceremony, highlighted by a red carpet. Individuals are dressed in elegant suits and bow ties, with their faces obscured for privacy. One person is using a smartphone, which could indicate they’re taking a photo or browsing messages. No mathematical or academic content is depicted"
        # prompts= {"49df59f6-2d63-4628-9ade-078beeb87e8d.png":img_file_des,"e3f4c333-abdb-4832-9d29-866a68444bbc.png":img_file_des,"test1.png":img_file_des,"test2.png":img_file_des}
        response = make_response(images, 200)
        return _corsify_actual_response(response)


@app.route("/set_path", methods=["POST", "OPTIONS"])
def set_path():
    global image_file_path, n_images
    if request.method == "OPTIONS":  # CORS preflight
        return _build_cors_preflight_response()
    else:
        status_code = 200
        image_file_path = request.get_json().get("image_file_path")
        n_images = int(request.get_json().get("n_images"))
        image_file_path = secure_filename(image_file_path)
        if image_file_path == "":
            response_txt = {"txt": "No directory path provided"}
            status_code = 404
            response = make_response(jsonify(response_txt), status_code)
            return response

        n_images = n_images if n_images > 0 else 1

        return redirect(url_for("prompt"))


@app.route("/prompt", methods=["GET", "OPTIONS"])
def prompt():
    if request.method == "OPTIONS":  # CORS preflight
        return _build_cors_preflight_response()
    elif image_file_path != "":
        return render_template("prompt.html")
    else:
        return redirect(url_for("index"))


@app.route("/get_image/<img_file>", methods=["GET", "OPTIONS"])
def get_image(img_file):
    if request.method == "OPTIONS":  # CORS preflight
        return _build_cors_preflight_response()
    else:
        img_file = secure_filename(img_file)
        print(img_file)
        if img_file != "":
            img_file = f"./outputs/{img_file}"
            if exists(img_file):
                status_code = 200
                response = send_file(img_file, mimetype="image/jpeg")
            else:
                status_code = 404
                response = make_response(
                    jsonify({"txt": "Image not found"}), status_code
                )
        else:
            status_code = 403
            response = make_response(
                jsonify({"txt": "Invalid image file name"}), status_code
            )
        return _corsify_actual_response(response)


def _build_cors_preflight_response():
    response = make_response()
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add("Access-Control-Allow-Headers", "Content-Type")
    response.headers.add("Access-Control-Allow-Methods", "POST, GET, PUT")
    return response


def _corsify_actual_response(response):
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response


if __name__ == "__main__":
    FlaskUI(app=app, server="flask", width=750, height=1080, port=5000).run()
