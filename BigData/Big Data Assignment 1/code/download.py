import http.client
import ssl
from datetime import datetime
import csv
import pymongo

ssl._create_default_https_context = ssl._create_unverified_context

# Connect to MongoDB
mongo_client = pymongo.MongoClient("mongodb://mongo:27017/")  # mongo is the name of the MongoDB service in docker-compose.yml
weather_db = mongo_client["weather"]
weather_collection = weather_db["weather_data"]

conn = http.client.HTTPSConnection("weatherapi-com.p.rapidapi.com")

headers = {
    'X-RapidAPI-Key': "cc34bd3499mshdf70e38c411074ep112e33jsnbab6d4a91948",
    'X-RapidAPI-Host': "weatherapi-com.p.rapidapi.com"
}

# Open the CSV file
with open('Top100-US.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile, delimiter=';')
    
    for row in reader:
        zip_code = row['Zip']
        city = row['City']

        conn.request("GET", f"/current.json?q={zip_code}", headers=headers)
        res = conn.getresponse()
        weather_data = res.read().decode("utf-8")

        # Store data in MongoDB
        entry = {
            "zip": zip_code,
            "city": city,
            "weather": weather_data,
            "created_at": datetime.now()
        }
        weather_collection.insert_one(entry)
        print("Data stored in MongoDB for", city)

print("Script finished successfully")
