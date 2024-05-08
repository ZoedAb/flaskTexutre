from flask import Flask, jsonify, request
from trello_bot import main,sendImage
from model import generate
app = Flask(__name__)
DRIVER = None
# Example data
items = [
    {"id": 1, "name": "Item 1"},
    {"id": 2, "name": "Item 2"}
]

@app.route('/api/items', methods=['GET'])
def get_items():
    result = sendImage()
    return jsonify(result = result)

@app.route('/api/items', methods=['POST'])
def run_script():
    print("hello")
    task = request.json.get('task')
    print(task)
    result = main(task=task)
    return jsonify(result = result)

@app.route('/api/model', methods=['POST'])
def run_model():
    print("hello")
    task = request.json.get('task')
    print(task)
    result = generate(prompt=task)
    return jsonify(result = result)
if __name__ == '__main__':
    app.run(debug=True)
