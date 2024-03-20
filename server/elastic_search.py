import datetime

#ES
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk

#embeddings
import embs as embs

import settings as settings

#instantiate and return an elastic search client
def get_client():
    client = Elasticsearch(
        "https://localhost:9200",
        ssl_assert_fingerprint=settings.CERT_FINGERPRINT,
        basic_auth=("elastic", settings.ELASTIC_PASSWORD)
    )
    
    return client 

#Creates a new index in Elastic search
#and uploads chunks of board game manual, with corresponding vectors
def new_game_index(es_client, index, game_name, chunks):
    if es_client.indices.exists(index=index):
        raise Exception(f"Cannot create index. Index '{index}' already created.")

    properties = {
        "my_vector": {
        "type": "dense_vector",
        "dims": 384,
        "similarity": "dot_product",
        "index": True
        # "index_options": {
        #     "type": "int8_hnsw"
        # }
        }
    }
    es_client.indices.create(index=index)
    
    es_client.indices.put_mapping(index=index, properties=properties)

    #Set up text embedding model:
    embeddings_model = embs.initialize_embeddings_model()

    embeddings = embeddings_model.embed_documents(chunks)
    text_embeddings = zip(chunks, embeddings)

    #create documents for ElasticSearch
    docs_for_elasticsearch = []
    for text, embedding in text_embeddings:
        doc = {
            '_index': index,
            '_source': {
                'game': game_name,
                'text': text,
                'my_vector': embedding,
                'timestamp': datetime.datetime.now()
            }}
        docs_for_elasticsearch.append(doc)
    
    response = bulk(es_client, docs_for_elasticsearch)


#queries elastic search index for relevant text chunks
def query_elastic_search_by_index(es_client, index, user_question):    
    embeddings_model = embs.initialize_embeddings_model()    
    embedded_question = embeddings_model.embed_documents([user_question])[0]

    #dense vector search (essentially semantic search)
    search = {
    "knn": {
        "field": "my_vector",
        "query_vector": embedded_question,
        "k": 3,
        "num_candidates": 100
    },
    "fields": [ "text" ]
    }

    #Simple match query:
    # query = {
    #     "query": {
    #         "match": {
    #         "text": {
    #             "query": user_question,
    #             "minimum_should_match": "10%"
    #         }
    #         }
    #     }}

    response = es_client.search(index=index, body=search)
    hits = response['hits']['hits']
    contexts = []
    for hit in hits: 
        context = hit['_source']['text']
        print(context)
        contexts.append(context)
    
    return contexts