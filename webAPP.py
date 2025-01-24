# Hier komt de webAPP die alles linkt (ofwel de API)
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    return "Welcome to the Flask API!"

@app.route("/check_answer", methods=["POST"])
def check_answer():
    # Example logic for checking an answer
    data = request.get_json()
    student_answer = data.get("answer")
    correct_answer = data.get("correct_answer")

    if student_answer == correct_answer:
        return jsonify({"message": "Correct!", "status": "success"})
    else:
        return jsonify({"message": "Incorrect, check your calculations.", "status": "error"})

if __name__ == "__main__":
    app.run(debug=True)
