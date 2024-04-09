import datetime
from pypdf import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter

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
    print(f"Connected to ElasticSearch cluster `{client.info().body['cluster_name']}`")
    return client

def new_game_index(es_client, pdf_path, index=None):
    try:
        reader = PdfReader(pdf_path)
    except Exception:
        raise Exception(f"File at path: {pdf_path} could not be read") 

    pdf_content = ""
    for page in reader.pages:
        text = page.extract_text()
        pdf_content += text

    text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
        chunk_size=512, chunk_overlap=256
    )
    docs = text_splitter.create_documents([pdf_content])

    # Define the new elasticsearch index
    mappings = {
        "properties": {
            "content": {
                "type": "text"
            },
            "content_vector": {
                "type": "dense_vector",
                "dims": 384,
                "index": "true",
                "similarity": "cosine"
            }
        }
    }

    #if an index is specified in args, hardcode the index, otherwise, create new index using datetime
    if index is None:
        index = "index_" + datetime.datetime.now().strftime("%Y%m%d%H%M%S")

    try:
        es_client.indices.create(index=index, mappings=mappings)
    except Exception as e:
        raise Exception(f"Could not create new ElasticSearch index: {index}") 

    # Initialize the embeddings model
    embeddings_model = embs.initialize_embeddings_model()
    # embeddings = embeddings_model.embed_documents(docs)

    # Bulk insert the documents into the index
    operations = []
    for doc in docs:
        operations.append({"index": {"_index": index}})
        doc_object = {
            "content": doc.page_content,
            # Transforming the title into an embedding using the model
            "content_vector": embeddings_model.embed_documents([doc.page_content])[0]
        }
        operations.append(doc_object)
    response = es_client.bulk(index="root_index", operations=operations, refresh=True)
    inserted = response["items"]
    print(f"Created index {index} with {len(inserted)} documents")

    return index


#queries elastic search index for relevant text chunks
def query_elastic_search_by_index(es_client, index, user_question, hits=3):    
    embeddings_model = embs.initialize_embeddings_model()    
    embedded_question = embeddings_model.embed_documents([user_question])[0]

    #dense vector search (essentially semantic search)
    response = es_client.search(
        index=index,
        knn={
            "field": "content_vector",
            "query_vector": embedded_question,
            "k": hits,
            "num_candidates": 100,
        },
    )

    hits = response['hits']['hits']
    contexts = []
    # contexts = []
    for hit in hits: 
        context = hit['_source']['content']
        #print("Context from ES:", context)
        contexts.append(context)
    
    return contexts