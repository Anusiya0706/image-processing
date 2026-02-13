from flask import Flask, redirect, url_for, render_template, request
from werkzeug.utils import secure_filename
import os
import cv2

app = Flask(__name__)
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(APP_ROOT, 'static')


@app.route('/prediction', methods=['GET', 'POST'])
def prediction():
    if request.method == 'POST':
        file = request.files.get('image')
        if file and file.filename:
            filename = secure_filename(file.filename)
            save_path = os.path.join(STATIC_DIR, 'input.jpg')
            # always overwrite to keep template references simple
            file.save(save_path)

            # read and process
            image = cv2.imread(save_path, cv2.IMREAD_COLOR)
            if image is None:
                return render_template('index.html', error='Could not read uploaded image')
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            (thresh, im_bw) = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

            cv2.imwrite(os.path.join(STATIC_DIR, 'gray.jpg'), gray)
            cv2.imwrite(os.path.join(STATIC_DIR, 'binary.jpg'), im_bw)

            return render_template('index.html')

    return render_template('index.html')


@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(port=5000, debug=True)
