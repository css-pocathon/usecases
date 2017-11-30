import yaml
import json
import nltk
import requests
from nltk.draw.tree import draw_trees
from config import config

def get_sentiment(message, language):
    r = requests.post(config["TEXT_ANALYSIS_API_URL"]+"/sentiment",
    json={
        "documents":
        [
            {
                "language": language,
                "id": "0",
                "text": message
            }
        ]
    },
    headers = {
        "Ocp-Apim-Subscription-Key": config['TEXT_ANALYSIS_API_KEY'],
    })
    return json.loads(r.text)["documents"][0]["score"]

def detect_language(message):
    r = requests.post(config["TEXT_ANALYSIS_API_URL"]+"/languages",
    json={
        "documents": 
        [
            { 
                "id": "1", 
                "text": message 
            },
        ]
    },
    headers = {
        "Ocp-Apim-Subscription-Key": config['TEXT_ANALYSIS_API_KEY'],
    })
    return json.loads(r.text)["documents"][0]["detectedLanguages"][0]["iso6391Name"]

if __name__ == "__main__":
    assert get_sentiment("Ich finde dich sehr toll.") > 0.5, "Wasn't able to get sentiment right"
    assert detect_language("Ich spreche Deutsch.") == "de", "Wasn't able to classify German"
