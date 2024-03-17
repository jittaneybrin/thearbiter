from elasticsearch import Elasticsearch as es
from datetime import datetime
from sentence_transformers import SentenceTransformer
from elasticsearch_dsl import Search
 


ELASTIC_PASSWORD = "8Eu31vWSnMSOJrwK06qu"
CERT_FINGERPRINT = "15119ccd6b9a0e37eee39e36f878c99d2ef8048cf17e7f3221f1ac8ce19e24ca"

client = es(
    "https://localhost:9200",
    ssl_assert_fingerprint=CERT_FINGERPRINT,
    basic_auth=("elastic", ELASTIC_PASSWORD)
)


# Get all records from an index named 'your_index'
#result = client.search(index='fun_game', body={})

# #specific query
# result = client.search(index='fun_game', body={
#     "query": {
#         "match": {
#             "text": "monopoly"
#         }
#     }
# })

# body = {
#   "query": {
#     "more_like_this": {
#       "fields": ["text"],
#       "like": "me food",
#       "min_term_freq": 0,
#       "min_doc_freq": 1,
#       "max_query_terms": 25
#     }
#   }
# }
# result = client.search(index='test', body=body)



model = SentenceTransformer('bert-base-nli-mean-tokens')
sentences = ['what is for dinner']
vectors = model.encode(sentences)

# result = client.search(index='test', body={
#     "query": {
#         "more_like_this": {
#             "fields": ['text'],
#             "like": "mac and cheese",
#             "min_term_freq": 0,
#         }
#     }
# })
# print(result)

#Display the results
# for hit in result['hits']['hits']:
#     print(hit['_source'])




s = Search(using=client, index='test').query(
    "script_score",
    query={
        "match_all": {}
    },
    script={
        "source": "cosineSimilarity(params.query_vector, 'your_vector') + 1.0",
        "params": {"query_vector": vectors[0].tolist()}
    }
)

# Execute the search query
response = s.execute()

# Display the search results
for hit in response.hits:
    print(hit.meta.score, hit.meta.id, hit.text)