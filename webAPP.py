                                                                   # Hier komt de webAPP die alles linkt (ofwel de API)
from flask import Flask, request, jsonify                          # Dit zorgt voor de framework en het vertalen van data
import vragenscript as vs                                          # Dit creërt en checkt de vragen
import AI_mode as ai                                               # Dit is het AI model, die ik per ongeluk AI_mode heb genoemd
                                                                   
app = Flask(__name__)                                              
                                                                   
@app.route("/vraag_maken", methods=["GET"])                        # Dit heeft iets te maken met welke functie gekozen wordt (AANPASSEN)
def vragen():                                                      
    try:                                                           
        """                                                        
        Hier wordt een vraag gevormd op basis van de informatie die uit de database geleverd wordt
        """                                                        
                                                                   
        difficulty = request.args.get("difficulty", "Beginner")    # Vraagt om de difficulty, waarbij Beginner standaard is (best handig dit)
        informatie = request.args.get("informatie", [1, 1, 1, 1])  # Vraagt om het succesaantal per vraagtype, met als standaard alles hetzelfde (mogelijk aanpassen om beter te maken)
        question = vs.keuze(informatie, difficulty)                # Deze code kiest de vraag. Functie is keuze(succesaantal, difficulty)
                                                                   
        return jsonify({                                           # Maakt het een json bestand van wat ik heb weten te vinden, veel code is online gevonden en met copilot en dergelijke geschreven
            "status": "success",                                   # Als het gelukt is krijg je een status bericht waarmee de server weet wat er gaande is. Ook wordt de vraag doorgestuurd
            "question": question                                   # Vraag wordt verzonden
        })                                                         
                                                                   
    except Exception as e:                                         # Als het faalt, dan wordt niks doorgestuurd en moet de pagina herladen
        return jsonify({"status": "error"}), 500                   # De status geeft aan dat er iets fout is gegaan. Error 500: internal server error                                               
                                                                                                                                   
@app.route("/vraag_nakijken", methods=["POST"])                    
def check_answer():                                                
    """                                                            
    Hier wordt het antwoord van de leerling nagekeken en, indien het antwoord fout is, zal de AI de berekeningen nakijken
    """                                                            
    try:                                                           
        data = request.get_json()                                  # De inkomende data ophalen. Deze wordt opgesplitst in berekeningen, studenten_antwoord en probleem
        student_calc = data.get("berekeningen")                    # Berekeningen van de student
        student_answer = data.get("studenten_antwoord")            # Het antwoord van de student  
        question = data.get("probleem")                            # De vraag die de student kreeg
        correct = vs.check(question, student_answer)               # Vraag wordt nagekeken. Functie is check(gekozen_vraag, studenten_antwoord)
                                                                   
        if correct:                                                
            return jsonify({                                       
                "status": "success"                                # Vraag is goed beantwoord, de AI zal niks hoeven doen            
            })                                                     
                                                                   
        else:                                                                  
            mistakes = ai.analyze_calculations(student_calc)       # Vraag is fout beantwoord, de AI kijkt alles na (ook eindantwoord als deze bij de berekeningen staat)
                                                                   #
            return jsonify({                                       # Antwoorden worden teruggestuurd
                "status": "wrong",                                 # Vraag is fout beantwoord
                "mistakes": mistakes                               # Fout soorten worden teruggestuurd
            })                                                     
                                                                   
    except Exception as e:                                         # Fout melding (deze zal vaak voorkomen indien leerlingen niet juist de antwoorden opschrijven
        return jsonify({"status": "error"}), 500                                                    
                                                                                                                      
if __name__ == "__main__":                                         # Debug mode, indien we dat nodig hebben
    app.run(debug=True)                                            
