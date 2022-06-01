import requests


def getWordDefinition(word):
    new_dict_data = {}
    URL_Address = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
    response = requests.get(URL_Address)
    if response.status_code == 200:
        data = response.json()[0]
        try:
            if data['phonetics'][0].get('audio'):
                audio = data['phonetics'][0]['audio']
                new_dict_data['audio'] = audio
        finally:
            definitions = data['meanings'][0]['definitions']
            new_dict_data['definitions'] = "\n".join([f"✔ {definition['definition']}." for definition in definitions])
            return new_dict_data
    else:
        return False


getWordDefinition("mother")
