from pymongo import MongoClient
from urllib.parse import quote_plus
username=quote_plus("varsha_admin")
password=quote_plus("Tanishk@2005")

uri = f"mongodb+srv://varsha_admin:Tanishk@2005@cluster0.aozvrql.mongodb.net/?appName=Cluster0"

print("Connected Successfully!")

