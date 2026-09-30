import os
from pathlib import Path
from dotenv import load_dotenv
from pymongo import MongoClient

env_path = Path(__file__).resolve().parent / ".env"
load_dotenv(dotenv_path=env_path)

usuario = os.getenv("MONGO_USER")
password = os.getenv("MONGO_PASSWORD")
cluster = os.getenv("MONGO_CLUSTER")
database = os.getenv("MONGO_DB")
collection_name = os.getenv("MONGO_COLLECION")

if not all([usuario, password, cluster, database, collection_name]):
    raise Exception("Por favor establecer todas las variables de entorno")

uri = f"mongodb+srv://{usuario}:{password}@{cluster}/"

cliente = MongoClient(uri)

db = cliente[database]

collection = db[collection_name]