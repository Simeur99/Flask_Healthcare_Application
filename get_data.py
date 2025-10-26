from flask import Flask, render_template, request, redirect
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import os
from dotenv import load_dotenv

app = Flask(__name__)  # Initialize Flask app
#connect to MongoDBAtlas
uri = os.getenv("uri")

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

db = client["survey_db"]  # Create/use database
collection = db["user_data"]  # Create/use collection

@app.route('/')
def index():
    # Render the form page
    return render_template('form.html')

@app.route('/submit', methods=['POST'])
def submit():
    data = {
        "name": request.form.get("name"),
        "email": request.form.get("email"),
        "phone": request.form.get("phone"),
        "age": request.form.get("age"),
        "gender": request.form.get("gender"),
        "income": float(request.form.get("income")),
        "totalExpenses": float(request.form.get("totalExpenses")),
        "expenses": {}
    }

    expense_categories = ["utilities", "entertainment", "schoolFees", "shopping", "healthcare", "others"]
    for category in expense_categories:
        checkbox = request.form.get(category)
        amount = request.form.get(f"{category}_amount")
        if checkbox and amount:
            data["expenses"][category] = float(amount)
        else:
            data["expenses"][category] = 0.0

    collection.insert_one(data)
    print("Data inserted:", data)
    return redirect('/')
    # Save to MongoDB

if __name__ == '__main__':
    app.run(debug=True)