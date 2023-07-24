import os
import requests
from flask import Flask, render_template, request
from jinja2 import Template

app = Flask(__name__, static_folder='static')
app.config["DEBUG"] = True

os.environ['EDAMAM_APP_ID'] = '4ba2acf1'
os.environ['EDAMAM_APP_KEY'] = '984e714dc4b8dee2ecf753e1b72dec20'

@app.route('/')
def navbar():
    return render_template('navbar.html')

@app.route('/recipes')
def search():
    ingredient = request.args.get('ingredient')

    hits = edamam_search(ingredient)

    return render_template('recipes.html', ingredient=ingredient, hits=hits)

def edamam_search(query):
    # Access the Edamam App ID and App Key from the environment variables
    app_id = os.environ['EDAMAM_APP_ID']
    app_key = os.environ['EDAMAM_APP_KEY']

    curl = f"https://api.edamam.com/search?q={query}" \
           f"&app_id={app_id}" \
           f"&app_key={app_key}"

    response = requests.get(curl)
    if response.status_code == 200:
        data = response.json()
        hits = data.get('hits', [])
    else:
        hits = []  # Return an empty list if the API request failed

    return hits

if __name__ == '__main__':
    app.run()
