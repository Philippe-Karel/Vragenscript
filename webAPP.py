# Hier komt de webAPP die alles linkt (ofwel de API)
from flask import Flask, request, jsonify   # Dit zorgt voor de framework en het vertalen van data
import vragenscript as vs                   # Dit creërt en checkt de vragen
import AI_mode as ai                        # Dit is het AI model, die ik per ongeluk AI_mode heb genoemd

app = Flask(__name__)

@app.route("/generate_question", methods=["GET"])
def vragen(): 
    try:
        difficulty = request.args.get("difficulty", "Beginner")  # Vraagt om de difficulty, waarbij Beginner standaard is (best handig dit)
        informatie = request.args.get("informatie", [1, 1, 1, 1])
        question = vs.keuze(difficulty)                          # Deze code kiest een vraag

        return jsonify({
            "status": "success",
            "question": question
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Error generating question: {str(e)}"
        }), 500


@app.route("/check_answer", methods=["POST"])
def check_answer():
    """
    Check a student's answer and calculations.
    """
    try:
        # Parse incoming JSON data
        data = request.get_json()
        student_calc = data.get("calculation")  # Student's calculations
        student_answer = data.get("answer")    # Student's final answer
        correct_answer = data.get("correct_answer")  # Correct answer from the database

        # Step 1: Check the student's answer using the question-checking script
        is_correct = qs.check_answer(student_calc, student_answer, correct_answer)

        if is_correct:
            return jsonify({
                "status": "success",
                "message": "Well done! Your answer is correct."
            })
        else:
            # Step 2: Use the AI to analyze student calculations
            mistakes = ai.analyze_calculations(student_calc, correct_answer)

            return jsonify({
                "status": "error",
                "message": "Your answer is incorrect.",
                "mistakes": mistakes
            })
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Error checking answer: {str(e)}"
        }), 500


if __name__ == "__main__":
    app.run(debug=True)
