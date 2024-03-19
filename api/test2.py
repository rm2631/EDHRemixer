import requests

root = "https://api.scryfall.com/"

endpoint = "/cards/search"


response = requests.get(root + endpoint, params={"q": "Mountain", "dir": "Auto"})

response.json()["data"][0]["id"]
response.json()["data"][0]["name"]
response.json()["data"][0]["color_identity"]
