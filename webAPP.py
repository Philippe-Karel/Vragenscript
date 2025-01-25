from flask import Flask, request, jsonify
import vragenscript as vs  # Module to generate and check questions
import AI_mode as ai  # Module for AI analysis of student calculations

app = Flask(__name__)

# Endpoint to generate a question
@app.route("/vraag_maken", methods=["GET"])
def generate_question():
    try:
        # Retrieve parameters from the request, with default values
        difficulty = request.args.get("difficulty", "Beginner")  # Default difficulty: Beginner
        informatie = request.args.getlist("informatie", type=int)  # List of success counts per question type

        # If no specific information is provided, use default values [1, 1, 1, 1]
        if not informatie:
            informatie = [1, 1, 1, 1]

        # Generate the question using the vragenscript module
        question = vs.keuze(informatie, difficulty)  # Function keuze(succesaantal, difficulty)

        # Return the generated question as JSON
        return jsonify({
            "status": "success",
            "question": question
        })

    except Exception as e:
        # Handle errors gracefully and return an error response
        return jsonify({"status": "error", "message": str(e)}), 500

# Endpoint to check a student's answer and analyze their calculations if needed
@app.route("/vraag_nakijken", methods=["POST"])
def check_answer():
    try:
        # Retrieve JSON data from the request
        data = request.json

        # Validate that all required fields are present
        if not data or 'berekeningen' not in data or 'student_antwoord' not in data or 'vraag' not in data:
            return jsonify({"status": "error", "message": "Missing required fields"}), 400

        # Extract relevant data from the request
        student_calc = data.get("berekeningen").replace("**", "^")  # Student's calculations (adjusted for syntax)
        student_answer = data.get("student_antwoord")  # Student's final answer
        question = data.get("vraag")  # The question the student attempted

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
            # Analyze the student's calculations using the AI model
            mistakes = ai.analyze_calculations(student_calc)

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
    # Run the Flask app in debug mode for development purposes
    app.run(debug=True)
