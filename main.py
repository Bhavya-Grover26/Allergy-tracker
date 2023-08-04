import os
import requests
import pickle
import pandas as pd
from flask import Flask, render_template, request , jsonify, session, redirect, url_for
from jinja2 import Template
from py_edamam import PyEdamam 
from collections import deque
from flask_pymongo import PyMongo
from pymongo import MongoClient

app = Flask(__name__, static_folder='static')
app.config["DEBUG"] = True

os.environ['EDAMAM_APP_ID'] = '4ba2acf1'
os.environ['EDAMAM_APP_KEY'] = '345f58077c89160ac3c67e636bbda828'

url = "https://api.humanapi.co/v1/human/medical/allergies"

headers = {
    "accept": "application/json",
    "Authorization": "Bearer <<public_at>>"
}

response = requests.get(url, headers=headers)

print(response.text)

data = pd.read_csv("FoodData.csv")

# Define the Node class for the linked list
class Node:
    def __init__(self, food, allergy):
        self.food = food
        self.allergy = allergy
        self.next = None

# Define the LinkedList class
class LinkedList:
    def __init__(self):
        self.head = None

    def insert(self, food, allergy):
        new_node = Node(food, allergy)
        new_node.next = self.head
        self.head = new_node

    def search(self, food):
        current_node = self.head
        while current_node:
            if current_node.food.lower() == food.lower():  # Case-insensitive comparison
                return current_node.allergy
            current_node = current_node.next
        return "No allergy information available"

# Function to read CSV and create the linked list
def read_csv_and_create_linked_list(csv_file):
    linked_list = LinkedList()
    with open(csv_file, 'r') as file:
        lines = file.readlines()
        for line in lines[1:]:  # Skip the header line
            class_, type_, group, food, allergy = line.strip().split(',')
            linked_list.insert(food, allergy)
    return linked_list

def save_linked_list_to_file(linked_list, file_name):
    with open(file_name, 'wb') as file:
        pickle.dump(linked_list, file)

# Load the linked list from the saved file
def load_linked_list_from_file(file_name):
    with open(file_name, 'rb') as file:
        linked_list = pickle.load(file)
    return linked_list

class SymptomNode:
    def __init__(self, symptom, food):
        self.symptom = symptom
        self.food = food
        self.next = None

class SymptomLinkedList:
    def __init__(self):
        self.head = None

    def add_node(self, symptom, food):
        new_node = SymptomNode(symptom, food)
        if not self.head:
            self.head = new_node
            return
        current = self.head
        while current.next:
            current = current.next
        current.next = new_node
    
    def __iter__(self):
        current = self.head
        while current:
            yield current
            current = current.next



@app.route('/index')
def display_linked_list():
    linked_list = load_linked_list_from_file('linked_list_data.pickle')

    # Convert the linked list data to a pandas DataFrame
    data = []
    current_node = linked_list.head
    item_number = 1
    while current_node:
        data.append([item_number, current_node.food, current_node.allergy])
        current_node = current_node.next
        item_number += 1

    df = pd.DataFrame(data, columns=['Item Number', 'Food', 'Allergy'])

    # Convert the DataFrame to an HTML table
    table_html = df.to_html(index=False)

    return render_template('index.html', table_html=table_html)


@app.route('/')
def navbar():
    return render_template('dashboard.html')

app.config ["SECRET_KEY"] = "56f7c18ca74b1712ba94242c40ccef435d1fa4ac"
app.config["MONGO_URI"] = "mongodb+srv://chinmayidotdesai:digitaldreamers@cluster0.j61lfnm.mongodb.net/Allergy-tracker?retryWrites=true&w=majority"

mongo = PyMongo()
mongo = PyMongo(app)

client = MongoClient('mongodb+srv://chinmayidotdesai:digitaldreamers@cluster0.j61lfnm.mongodb.net/?retryWrites=true&w=majority')
db = client["Allergy-tracker"]
collection = db["Allergy-tracker"]

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')

    user_data = {
        'username': username,
        'email': email,
        'password': password
    }

    # Insert user data into MongoDB
    collection = mongo.db.users
    collection.insert_one(user_data)

    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user_data = {
            'username': username,
            'password': password
        }

        # Check user credentials against MongoDB
        collection = mongo.db.users
        user = collection.find_one(user_data)

        if user:
            session['username'] = user['username']
            return redirect(url_for('navbar'))  # Redirect to dashboard route
        else:
            error_message = "Invalid credentials. Please try again."
            return render_template('login.html', error_message=error_message)

    return render_template('login.html')  # For GET requests


@app.route('/recipes')
def search():
    ingredient = request.args.get('ingredient')

    # Call the edamam_search function to get the list of recipes
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
    recipes_with_allergies = []
    if response.status_code == 200:
        data = response.json()
        hits = data.get('hits', [])
        # Extract the list of ingredients for each recipe
        linked_list = load_linked_list_from_file('linked_list_data.pickle')
        for hit in hits:
            recipe = hit.get('recipe', {})
            label = recipe.get('label', '')
            image = recipe.get('image', '')
            url = recipe.get('url', '')
            ingredients = recipe.get('ingredientLines', [])
            matched_ingredients_with_allergies = []
            for ingredient in ingredients:
                words = ingredient.split()  # Split ingredient into individual words
                matching_words = [word for word in words if linked_list.search(word) != "No allergy information available"]
                if matching_words:
                    matched_ingredient = " ".join(matching_words)
                    allergy = linked_list.search(matched_ingredient)
                    matched_ingredients_with_allergies.append({'ingredient': matched_ingredient, 'allergy': allergy})
            if matched_ingredients_with_allergies:
                recipes_with_allergies.append({'label': label, 'image': image, 'url': url, 'ingredients_with_allergies': matched_ingredients_with_allergies})

    return recipes_with_allergies

@app.route('/symptom', methods=['GET', 'POST'])
def select_symptom():
    symptom_list = SymptomLinkedList()

    # Read CSV file using pandas
    df = pd.read_csv('FoodSymptoms.csv')

    # Iterate through the DataFrame and add nodes to the linked list
    for index, row in df.iterrows():
        symptom = row['Symptom']
        food = row['Allergy']
        symptom_list.add_node(symptom, food)

    selected_foods = []

    if request.method == 'POST':
        selected_symptoms = request.form.getlist('symptom')
        current = symptom_list.head
        while current:
            if current.symptom in selected_symptoms:
                selected_foods.append(current.food)
            current = current.next

    return render_template('symptom_checker.html', symptom_list=symptom_list, selected_foods=selected_foods)


if __name__ == '__main__':
    csv_file = 'FoodData.csv'
    linked_list = read_csv_and_create_linked_list(csv_file)
    save_linked_list_to_file(linked_list, 'linked_list_data.pickle')

    # Initialize MongoDB connection
    mongo = PyMongo()
    mongo.init_app(app)

    app.run()







