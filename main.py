from flask import Flask, render_template
from flask_pymongo import PyMongo

app = Flask(__name__)
#app.config['MONGO_URI'] = 'mongodb://localhost:27017/your_database_name'
#mongo = PyMongo(app)

@app.route('/')
def navbar():
    return render_template('navbar.html')

if __name__ == '__main__':
    app.run(debug=True)