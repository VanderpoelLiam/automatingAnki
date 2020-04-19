#! python3

# ankiAPI.py - API to interact with Anki deck
# REQUIRES ANKI APP TO BE RUNNING IN THE BACKGROUND

import requests
import base64


def invoke(json):
    response = requests.post('http://127.0.0.1:8765', json = json)
    responseJson = response.json()

    if responseJson['error'] is not None:
        raise Exception(responseJson['error'])

    return responseJson['result']

def addNote(deck, fields):
    model = "All-Purpose Card"
    json={
        "action": "addNote",
        "version": 6,
        "params": {
            "note": {
                "deckName": deck,
                "modelName": model,
                "fields": fields,
                "tags": []
            }
        }
    }
    return(invoke(json))

def storeMediaFile(filename):
    with open(filename, "rb") as img:
        data = base64.b64encode(img.read())

    json = {
        "action": "storeMediaFile",
        "version": 6,
        "params": {
            "filename": filename,
            "data": data
        }
    }

    return(invoke(json))
