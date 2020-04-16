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
            "url": url
        }
    }
    return(invoke(json))

# url = "https://www.google.com/imgres?imgurl=https%3A%2F%2Fnatashaskitchen.com%2Fwp-content%2Fuploads%2F2017%2F04%2FHomemade-Sausage-2-600x900.jpg&imgrefurl=https%3A%2F%2Fnatashaskitchen.com%2Fhow-to-make-homemade-sausage-video%2F&tbnid=fmlCXs1txzc3bM&vet=12ahUKEwjmouKl0-3oAhVImp4KHehgCn8QMygBegUIARDUAg..i&docid=RrK28lPPmqI4LM&w=600&h=900&q=sausage&ved=2ahUKEwjmouKl0-3oAhVImp4KHehgCn8QMygBegUIARDUAg"
# filename = "2.png"
# print(storeMediaFile(filename, url))
# print(addNote(deck, fields))
