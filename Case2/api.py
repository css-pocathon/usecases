import requests
import json

def check_name(name):
    if name == "":
        return False
    r = requests.get("http://35.189.74.56/costumers/search/findByNameContainingIgnoreCase?name={name}".format(name=name))
    return len(json.loads(r.text)["_embedded"]["costumers"]) > 0

def check_surname(surname):
    if surname == "":
        return False
    r = requests.get("http://35.189.74.56/costumers/search/findBySurnameContainingIgnoreCase?surname={surname}".format(surname=surname))
    return len(json.loads(r.text)["_embedded"]["costumers"]) > 0

def get_id(surname):
    if surname == "":
        return False
    r = requests.get("http://35.189.74.56/costumers/search/findBySurnameContainingIgnoreCase?surname={surname}".format(surname=surname))
    return json.loads(r.text)["_embedded"]["costumers"][0]["_links"]["self"]["href"].split("/")[-1]

def check_phonenumber(surname, phonenumber):
    if phonenumber == "":
        return False
    r = requests.get("http://35.189.74.56/costumers/search/findBySurnameContainingIgnoreCase?surname={surname}".format(surname=surname))
    return json.loads(r.text)["_embedded"]["costumers"][0]["phone"].replace(" ", "") == phonenumber.replace(" ", "")