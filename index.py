import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import tensorflow 
import json
import vragenscript as vs
import numpy as np

from flask import Flask, request, jsonify
from flask_cors import CORS
from tensorflow.keras.preprocessing.text import Tokenizer, tokenizer_from_json
from tensorflow.keras.preprocessing.sequence import pad_sequences

app = Flask(__name__)
CORS(app)

# AI initialisen
MODEL_PATH = "AI/fouten_AI (1).keras"
ai = tensorflow.keras.models.load_model(MODEL_PATH)

# Tokenizer initialisen
TOKENIZER_PATH = "AI/tokenizer (1).json"
with open(TOKENIZER_PATH, 'r') as tok:
    tok_config = tok.read()
tokenizer = tokenizer_from_json(tok_config)

# Soorten fouten noteren voor de AI
soorten_fouten = [0, 1, 2, 3]

@app.route("/", methods=['GET'])
def home():
    return "<h1> Dit is de homepagina, hier hoor je niet te zijn </h1>"

# Endpoint to generate a question
@app.route("/vraag_maken", methods=["GET"])
def generate_question():
    try:
        # Retrieve parameters from the request, with default values
        difficulty = request.args.get("difficulty", "Beginner")  # Default difficulty: Beginner
        informatie = request.args.getlist("information", type=int)  # List of success counts per question type

        # If no specific information is provided, use default values [1, 1, 1, 1]
        if not informatie:
            informatie = [1, 1, 1, 1]

        # Generate the question using the vragenscript module
        question = vs.keuze(informatie, difficulty)  # Function keuze(succesaantal, difficulty)

        # Return the generated question as JSON
        return jsonify({
            "status": "success",
            "question": str(question)
        })

    except Exception as e:
        # Handle errors gracefully and return an error response
        return jsonify({"status": "error", "message": str(e)}), 500

# Endpoint to check a student's answer and analyze their calculation if needed
@app.route("/vraag_nakijken", methods=["POST"])
def check_answer():
    try:
        # Retrieve JSON data from the request
        data = request.get_json()

        # Validate that all required fields are present
        if not data or 'calculation' not in data or 'final_answer' not in data or 'question' not in data:
            return data
            #return jsonify({"status": "error", "message": "Missing required fields"}), 400

        # Extract relevant data from the request
        student_calc = data.get("calculation", "").replace("**", "^").replace(":", "/")  # Student's calculation (adjusted for syntax)
        student_answer = data.get("final_answer")  # Student's final answer
        question = data.get("question")  # The question the student attempted

        # Check the student's answer using vragenscript
        correct = vs.check(question, student_answer)  # Function check(gekozen_vraag, studenten_antwoord)

        if correct[-1] == True:  # If there's an error in the student's response format
            return jsonify({"status": "student_error", "message": "Invalid response format"}), 400

        elif correct[0] == True:  # If the answer is correct
            return jsonify({
                "status": "success",  # Indicates success
                "constante": correct[1]  # Additional information if needed
            })

        else:  # If the answer is incorrect
            calc_seq = tokenizer.texts_to_sequences(student_calc)
            calc_pad = pad_sequences(calc_seq, padding='post')
            mistakes_AI = ai.predict(calc_pad)
            mistakes = [ind for ind, waarde in enumerate(mistakes_AI) if waarde > 0.5]
            
            # Return the analysis results and mark the answer as wrong
            return jsonify({
                "status": "wrong",  # Indicates the answer is wrong
                "constante": correct[1],
                "mistakes": mistakes  # Feedback on calculation mistakes
            })

    except Exception as e:
        # Handle errors gracefully and return an error response
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
