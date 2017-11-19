from flask import Flask, send_from_directory, request, jsonify
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def main():
    if request.method == 'GET':
        return send_from_directory('frontend', 'index.html')
    return jsonify({"hello": "world"})

@app.route('/<path:file>')
def send(file):
    print(file)
    return send_from_directory('frontend', file)
