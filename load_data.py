import csv
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import os
from dotenv import load_dotenv

# Define the User class
class User:
    def __init__(self, doc):
        self.name = doc.get("name", "")
        self.email = doc.get("email", "")
        self.phone = doc.get("phone", "")
        self.age = doc.get("age", "")
        self.gender = doc.get("gender", "")
        self.income = doc.get("income", 0.0)
        self.expenses = doc.get("expenses", {})
        self.total_expenses = doc.get("totalExpenses", sum(self.expenses.values()))

#  Connect to MongoDB
uri = os.getenv("uri")
client = MongoClient(uri, server_api=ServerApi('1'))

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

db = client["survey_db"]
collection = db["user_data"]

#  Fetch all documents and create User objects
users = []
for doc in collection.find():
    user = User(doc)
    users.append(user)

# Step 4: Export to CSV
csv_file = "user_data.csv"
with open(csv_file, mode="w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)

    # Write header
    writer.writerow([
        "Name", "Email", "Phone", "Age", "Gender", "Income", "Total_Expenses",
        "expense_Utilities", "expense_Entertainment", "expense_School_Fees", 
        "expense_Shopping", "expense_Healthcare", "expense_Others"
    ])

    # Write each user's data
    for user in users:
        writer.writerow([
            user.name,
            user.email,
            user.phone,
            user.age,
            user.gender,
            user.income,
            user.total_expenses,
            user.expenses.get("utilities", 0.0),
            user.expenses.get("entertainment", 0.0),
            user.expenses.get("schoolFees", 0.0),
            user.expenses.get("shopping", 0.0),
            user.expenses.get("healthcare", 0.0),
            user.expenses.get("others", 0.0)
        ])