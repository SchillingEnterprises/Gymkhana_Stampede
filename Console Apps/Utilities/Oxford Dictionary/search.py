# for more information on how to install requests
# http://docs.python-requests.org/en/master/user/install/#install
import requests
import json
import credentials

search_term = input('What word would you like to lookup? ')

language = 'en'
region = 'us'
word_id = search_term

url1 = 'https://od-api.oxforddictionaries.com:443/api/v1/entries/' + language + '/' + word_id.lower()
url2 = 'https://od-api.oxforddictionaries.com:443/api/v1/entries/' + language + '/' + word_id.lower() \
       + '/synonyms;antonyms'

r1 = requests.get(url1, headers={'app_id': credentials.app_id, 'app_key': credentials.app_key})
r2 = requests.get(url2, headers={'app_id': credentials.app_id, 'app_key': credentials.app_key})

data1 = json.loads(r1.text)
data2 = json.loads(r2.text)

# Parsed data
print(search_term.casefold(), ":")

try:
    if r1.status_code is 200:
        for result in data1['results']:
            for lexicalEntry in result['lexicalEntries']:
                part_of_speech = lexicalEntry.get('lexicalCategory')
                print("Part of Speech:\n", part_of_speech, "\n" * 2)
                for entry in lexicalEntry['entries']:
                    for sense in entry['senses']:
                        definition = sense.get('definitions')
                        print("Definition of", search_term, ":\n", definition, "\n")
                        for example in sense['examples']:
                            sample_sentences = example.get('text')
                            print("Sample Sentence:\n", sample_sentences, "\n")
    else:
        print("R1: code {}\n".format(r1.status_code))

    if r2.status_code is 200:
        for result in data2['results']:
            for lexicalEntry in result['lexicalEntries']:
                for entry in lexicalEntry['entries']:
                    for sense in entry['senses']:
                        for synonym in sense['synonyms']:
                            synonyms = synonym.get('text')
                            print("Synonym to", search_term, ":\n", synonyms, "\n")
    else:
        print("R2: code {}\n".format(r2.status_code))

except KeyError:
    pass
