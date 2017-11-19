from flask import Flask, send_from_directory, request, jsonify
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def main():
    if request.method == 'GET':
        return app.send_static_file('frontend/index.html')
    return jsonify({"hello": "world"})

@app.route('/<path:path>')
def send(path):
    return send_from_directory('frontend', path)
