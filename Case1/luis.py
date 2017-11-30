import json
import requests
from config import config

def get_intent(message, language):
    r = requests.get(config["LUIS_URL"].format(
        app_id=config["LUIS_APP_ID_"+language], api_key=config["LUIS_API_KEY"], message=message)
    )
    return json.loads(r.text)["topScoringIntent"]

def get_all_intents():
    r = requests.get(config["LUIS_URL"].format(
        app_id=config["LUIS_APP_ID_"+"de"], api_key=config["LUIS_API_KEY"], message="message")
    )
    response = json.loads(r.text)["intents"]
    return [intent["intent"] for intent in response]

def add_utterance(language, intent, message):
    r = requests.post(config["LUIS_ADD_UTTERANCE_URL"].format(app_id=config["LUIS_APP_ID_"+language], version_id="0.1"),
    json={
        "text": message,
        "intentName": intent,
        "entityLabels":[]
    },
    headers = {
        "Ocp-Apim-Subscription-Key": "15195fb1aab4450e9b626f8e4f210c78",
    })
    return r.text

def train_model(language):
    r = requests.post(config["LUIS_TRAIN_MODEL_URL"].format(app_id=config["LUIS_APP_ID_"+language], version_id="0.1"),
    headers = {
        "Ocp-Apim-Subscription-Key": "15195fb1aab4450e9b626f8e4f210c78",
    })
    return r.text
if __name__ == "__main__":
    assert get_intent("Hallo")["intent"] == "greeting", "Hallo is classified wrong"
    assert get_intent("Tschüss")["intent"] == "goodbye", "Tschüss is classified wrong"