from flask import Flask, send_from_directory, request, jsonify, url_for
from calculator import calculate_positions, render_chart
import os
import uuid

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def main():
    if request.method == 'GET':
        return send_from_directory('frontend', 'index.html')
    results = None
    try:
        results = calculate_positions(request.data.decode('utf-8').split('\n'))
        if not "err" in results:
            randid = str(uuid.uuid4())
            render_chart(randid + '.png', results)
            results["img"] = randid + ".png"
    except Exception as exception:
        results = {"err": str(exception)}
    return jsonify(results)


@app.route('/<path:file>')
def send(file):
    print(file)
    return send_from_directory('frontend', file)


app.config["CACHE_TYPE"] = "null"


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.context_processor
def override_url_for():
    """
    Generate a new token on every request to prevent the browser from
    caching static files.
    """
    return dict(url_for=dated_url_for)


def dated_url_for(endpoint, **values):
    if endpoint == 'static':
        filename = values.get('filename', None)
        if filename:
            file_path = os.path.join(app.root_path,
                                     endpoint, filename)
            values['q'] = int(os.stat(file_path).st_mtime)
    return url_for(endpoint, **values)
