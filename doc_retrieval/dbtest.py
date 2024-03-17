from elasticsearch import Elasticsearch
from datetime import datetime
from sentence_transformers import SentenceTransformer
from elasticsearch.helpers import bulk



ELASTIC_PASSWORD = "8Eu31vWSnMSOJrwK06qu"
CERT_FINGERPRINT = "15119ccd6b9a0e37eee39e36f878c99d2ef8048cf17e7f3221f1ac8ce19e24ca"

client = Elasticsearch(
    "https://localhost:9200",
    ssl_assert_fingerprint=CERT_FINGERPRINT,
    basic_auth=("elastic", ELASTIC_PASSWORD)
)



# model = SentenceTransformer('bert-base-nli-mean-tokens')
# sentences = ['the dog walked', 'marty took the canine through the neighborhood', 'I eat mac and cheese']
# vectors = model.encode(sentences)
# print(vectors[0])
# docs = []
# for i, sentence in enumerate(sentences):
#     doc = {
#         '_index': 'test',
#         '_source': {
#             'text': sentence,
#             'vector': vectors[i].tolist()
#         }
#     }
#     docs.append(doc)
# response = bulk(client, docs)
# print(response)

# # Create a test document
# doc = {
#     'game': 'monopoly',
#     'text': 'monopoly is so cool',
#     'timestamp': datetime.now(),
# }

chess_index = "abe"
# resp = client.index(index=chess_index, body=doc)
# print(resp['result'])

# Get all records from an index named 'your_index'
# result = client.search(index='abe', body={})
# pass




# query = {
#     "query": {
#         "fuzzy": {
#             "text": {
#             "value": "Abraham Lincoln was shot dead in the theatre",
#             "fuzziness": "1000"
#             }
#         }
#     }
# }
query = {
  "query": {
    "match_phrase": {
      "text": {
        "query": "Abraham Lincoln was shot dead in the theatre",
        "slop": 100
      }
    }
  }
}
index = 'abe'
response = client.search(index=index, body=query)
pass