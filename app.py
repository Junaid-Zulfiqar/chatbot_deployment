from flask import Flask, render_template, request, jsonify
from chat import get_response
from flask_cors import CORS




app = Flask(__name__)
CORS(app)
@app.route('/', methods=['GET'])
def index_get():
    return render_template("base.html")

@app.route('/predict', methods=['POST'])
def predict():
    text = request.get_json().get("value")
    response,time = get_response(text.get("message"))
    print(time)
        
    message = {"answer":response,"msg_time":time}
    print(message)
    return message


if __name__ == "__main__":
    app.run(host="localhost", port=8000,debug=True)


