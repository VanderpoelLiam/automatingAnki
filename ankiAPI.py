#! python3

# ankiAPI.py - API to interact with Anki deck
# REQUIRES ANKI APP TO BE RUNNING IN THE BACKGROUND

import requests


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

def storeMediaFile(filename, url):
    json = {
        "action": "storeMediaFile",
        "version": 6,
        "params": {
            "filename": filename,
            "url": imgURL
        }
    }
    return(invoke(json))

# print(uploadImage(filename, imgURL))
# print(addNote(deck, fields))
