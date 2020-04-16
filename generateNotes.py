import requests

imgURL = "https://www.simplyrecipes.com/wp-content/uploads/2014/07/hard-boiled-eggs-horiz-800-600x400.jpg"
# TODO - generate a unique filename for each image
filename = "egg1.jpg"

deck = "Generated Deck"
model = "All-Purpose Card"
blankedOutSentence = 'Er ___ Medizin.'
picture = '<div><img src="' + filename + '"></div><div></div><div></div>'
definition = 'studieren'
back = 'studiert'
fullSentence = 'Er studiert Medizin.'
extraInfo = 'ʃ t u: d i: r t'

fields = {
    "Front (Example with word blanked out or missing)": blankedOutSentence,
    "Front (Picture)": picture,
    "Front (Definitions, base word, etc.)": definition,
    "Back (a single word/phrase, no context)": back,
    "The full sentence (no words blanked out)": fullSentence,
    "Extra Info (Pronunciation, personal connections, conjugations, etc)": extraInfo,
    'Make 2 cards? ("y" = yes, blank = no)': "y"
}

def invoke(json):
    response = requests.post('http://127.0.0.1:8765', json = json)
    responseJson = response.json()

    if responseJson['error'] is not None:
        raise Exception(responseJson['error'])

    return responseJson['result']

def addNote(deck, model, fields):
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

def uploadImage(filename, url):
    json = {
        "action": "storeMediaFile",
        "version": 6,
        "params": {
            "filename": filename,
            "url": imgURL
        }
    }
    return(invoke(json))

print(uploadImage(filename, imgURL))
print(addNote(deck, model, fields))
