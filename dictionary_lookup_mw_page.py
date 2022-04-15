import requests
import json
import sys
import pydoc
import argparse
import os
from mw_api_key import API_KEY


def clear():
    if os.name == "nt":
        os.system('cls')
    else:
        os.system('clear')
    

parser = argparse.ArgumentParser(
    description="A simple command line dictionary that takes a single positional argument, queries Merriam Webster's Collegiate Dictionary API and returns parts of speech and definitions for the queried words"
)
parser.add_argument('word',
                    help="The word to be searched.",
                    nargs="*")
arg = parser.parse_args()
query = " ".join(arg.word)

url = f"https://www.dictionaryapi.com/api/v3/references/collegiate/json/{query}?key={API_KEY}"

response = requests.get(url)

json_data = response.json()

try:
    json_data[0]["meta"]
except TypeError:
    print()
    print("Word not found")
    print()
    sys.exit()

# Uncomment to see raw json data
# print(json.dumps(json_data, indent=4))

# Build string to format pydoc.pager
display = "\n"

for index, value in enumerate(json_data):
    headword = json_data[index]["meta"]["id"]
    if headword[-2] == ":":
        display += headword[0:-2] + "\n"
    else:
        display += headword + "\n"
    if "fl" in json_data[index]:    
        display += json_data[index]["fl"] + "\n\n"
    for index, definition in enumerate(json_data[index]["shortdef"]):
        display += f"{index + 1}. {definition}\n"
        
    display += "\n---------------------\n"

pydoc.pager(display)

clear()




