import yaml
import random
import string
from flask import Flask
from flask import session
from flask import request
from flask import jsonify
from flask_cors import CORS, cross_origin
from luis import *
from text_analysis import *

languages = ["de", "en"]
intents = get_all_intents()
text_intent = {
    "de": {
        "not_classified": "Konnte nicht klassifiziert werden. Bitte geben Sie eine der untenstehenden Optionen an.",
        "illegal_entry": "Ungültige Eingabe",
        "added_utterance": "Zum Modell hinzugefügt"
    },
    "it": {
        "not_classified": "Non è stato possibile classificare. Inserire una delle seguenti opzioni.",
        "illegal_entry": "Ingresso non valido",
        "added_utterance": "Aggiunto al modello"
    }
}
app = Flask(__name__)
CORS(app)

@app.route("/")
def main():
    return "Hello World!"

@app.route("/api/send", methods=["GET", "POST"])
@app.route("/api/send/<string:message>", methods=["GET", "POST"])
def handle_message(message=None):
    if message.lower() in intents:
        language = "de"
    else:
        language = detect_language(message)
    if language not in text_intent.keys():
        return jsonify({
                    "intent":"",
                    "score":"",
                    "text": "I don't speak your language, sorry!",
                    "accurate": True
            })
    last_message = request.data.decode("utf-8")
    if last_message != "":
        last_message = json.loads(last_message)["last_message"]
        if message not in intents:
            return text_intent[language]["illegal_entry"]
        add_utterance(language, message, last_message)
        train_model(language)
        return text_intent[language]["added_utterance"]
    else:
        intent = get_intent(message, language)
        if intent["score"] < 0.4:
            not_classified = text_intent[language]["not_classified"]
            for i in range(len(intents)):
                not_classified += str(i) + ")" + intents[i] + "\n"
            return jsonify({
                    "intent":intent["intent"],
                    "score":intent["score"],
                    "text": not_classified,
                    "accurate": False
            })
        return jsonify({
            "intent": intent["intent"],
            "score": intent["score"],
            "text": "",
            "accurate": True
        })    


if __name__ == "__main__":
    app.run(debug=True, threaded=True)
