
# from pymongo.mongo_client import MongoClient

# uri = "mongodb+srv://anujpatel1761:Admin12345@cluster0.n18qy.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# # Create a new client and connect to the server
# client = MongoClient(uri)

# # Send a ping to confirm a successful connection
# try:
#     client.admin.command('ping')
#     print("Pinged your deployment. You successfully connected to MongoDB!")
# except Exception as e:
#     print(e)

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Fetch MongoDB URL
MONGO_DB_URL = os.getenv("MONGO_DB_URL")  # Correct key name
print("MongoDB URL:", MONGO_DB_URL)  # Debugging output
