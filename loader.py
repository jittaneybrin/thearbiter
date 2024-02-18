
from elasticsearch import Elasticsearch
import csv

ELASTIC_PASSWORD = "06Tv9FUtTxQ43sdNuSdU"
CERT_FINGERPRINT = "e01bcdaa455cbab53bd08776aa99a3263fd8fa6c8b18d933972e936408869d09"
kibana = 'eyJ2ZXIiOiI4LjEyLjEiLCJhZHIiOlsiMTcyLjE4LjAuMjo5MjAwIl0sImZnciI6ImUwMWJjZGFhNDU1Y2JhYjUzYmQwODc3NmFhOTlhMzI2M2ZkOGZhNmM4YjE4ZDkzMzk3MmU5MzY0MDg4NjlkMDkiLCJrZXkiOiJ6N0VadlkwQk5neUVfUTd1OXZmNDpZN2o3M2duQ1N1Q3NjRXd0V3JMbjR3In0='
MAX_SIZE = 15

es = Elasticsearch(
    "https://localhost:9200",
    ssl_assert_fingerprint=CERT_FINGERPRINT,
    basic_auth=("elastic", ELASTIC_PASSWORD)
)


print(f"Connected to ElasticSearch cluster `{es.info().body['cluster_name']}`")

with open("./Car details v3.csv", "r") as f:
    reader = csv.reader(f)
    for i, line in enumerate(reader):
        print(i)
        document = {
            "name": line[0],
            "engine": line[9],
            "year": line[1],
            "price": line[2],
        }
        es.index(index="cars", document=document)
