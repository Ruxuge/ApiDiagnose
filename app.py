import os

from flask import Flask, request, url_for
from flask_restful import Api
from google.cloud import automl, automl_v1

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "key.json"

UPLOAD_FOLDER = '/home/ruxuge/PycharmProjects/TeleMed_Api/uploads'
ALLOWED_EXTENSIONS = {'jpeg'}

app = Flask(__name__.split('.')[0])
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

api = Api(app)

@app.route('/')
def home():
    return 'Hello World'



@app.route('/api', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if request.files:
            file = request.files['image.jpeg']
            file.save('/home/ruxuge/PycharmProjects/TeleMed_Api/uploads/image.jpeg')
            res = diagnose('uploads/image.jpeg')
            return goodResponse(res)
        elif request.method == 'POST':
            return noValue()
    elif request.method != 'POST':
        return badRequest()


@app.route('/goodResponse')
def goodResponse(res):
    return res


@app.route('/badRequest')
def badRequest():
    return 'Bad Request'


@app.route('/noValue')
def noValue():
    return 'Image is require'


with app.test_request_context():
    print(url_for('goodResponse'))
    print(url_for('noValue'))
    print(url_for('badRequest'))
    print(url_for('home'))


def diagnose(path):
    project_id = "telemed-300210"
    model_id = "ICN2967249830855835648"

    file_path = path

    with open(file_path, 'rb') as ff:
        content = ff.read()

    prediction_client = automl_v1.PredictionServiceClient()

    model_full_id = automl.AutoMlClient.model_path(
        project_id, "us-central1", model_id)

    payload = {'image': {'image_bytes': content}}
    params = {}
    result = prediction_client.predict(name=model_full_id, payload=payload, params=params)
    print("Prediction results:")
    for result in result.payload:
        print("Predicted entity label: {}".format(result.display_name))
        print("\n")
        var = result.display_name
        return var


if __name__ == '__main__':
    app.run(host="127.0.0.1", port= 8080, debug=True)
