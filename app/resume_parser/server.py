from flask import Flask, request, jsonify
from ner_predict import predict_entities

app = Flask(__name__)

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    text = data.get('text', '')
    entities = predict_entities(text)
    return jsonify(entities)

if __name__ == '__main__':
    app.run(port=5001, debug=True)
