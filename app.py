from flask import Flask, request, jsonify
import base64
from pdf_to_img_pdf import PDF2IMGPDF
from flask_cors import CORS
import json


app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 16 * 1000 * 1000
CORS(app)


@app.route("/download-pdf", methods=["POST"])
def download_pdf():
    posted_data = json.loads(request.data)
    if not posted_data.get("images", []):
        resp = jsonify({"message": "No images in request"})
        resp.status_code = 400
        return resp
    resp = jsonify({"pdf": PDF2IMGPDF.img_to_pdf(posted_data.get("images"))})
    resp.status_code = 200
    return resp


@app.route("/upload-pdf", methods=["POST"])
def upload_pdf():
    # check if the post request has the file partx
    if "pdf" not in request.form:
        resp = jsonify({"message": "No pdf in the request"})
        resp.status_code = 400
        return resp
    if request.form.get("pdf") == "":
        resp = jsonify({"message": "No file selected for uploading"})
        resp.status_code = 400
        return resp
    pdf_bytes = request.form.get("pdf")
    if len(pdf_bytes) > 0:
        images = PDF2IMGPDF.convert_to_images(base64.b64decode(pdf_bytes.encode()))
        resp = jsonify({"images": PDF2IMGPDF.decode_images(images)})
        resp.status_code = 201
    else:
        resp = jsonify({"message": "Allowed file types are pdf"})
        resp.status_code = 400
    return resp


if __name__ == "__main__":
    app.run()
