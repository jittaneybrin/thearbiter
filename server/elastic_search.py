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
    
    return client

def new_game_index(es_client, pdf_path):
    reader = PdfReader(pdf_path)

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

    index = "index_" + datetime.datetime.now().strftime("%Y%m%d%H%M%S")

    es_client.indices.create(index=index, mappings=mappings)

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



def new_forum(es_client, questions, answers, game_id):

    # Define the new elasticsearch index
    mappings =  {
    "properties": {
        "question": {
            "type": "text"
        },
        "answer": {
        "type": "text"
        },
        "question_vector": {
            "type": "dense_vector",
            "dims": 384,
            "index": "true",
            "similarity": "cosine"
        },
        "answer_vector": {
            "type": "dense_vector",
            "dims": 384,
            "index": "true",
            "similarity": "cosine"
        }
    }
  }


    es_client.indices.create(index=game_id, mappings=mappings)

    # Initialize the embeddings model
    embeddings_model = embs.initialize_embeddings_model()
    # embeddings = embeddings_model.embed_documents(docs)

    # Bulk insert the documents into the index
    operations = []
    for count, question in enumerate(questions):
        operations.append({"index": {"_index": game_id}})
        question_answer_object = {
            "question": question,
            "answer": answers[count],
            # Transforming the title into an embedding using the model
            "question_vector": embeddings_model.embed_documents(question)[0],
            "answer_vector": embeddings_model.embed_documents(answers[count])[0],
        }
        operations.append(question_answer_object)

    response = es_client.bulk(index=game_id, operations=operations, refresh=True)
    inserted = response["items"]
    print(f"Created index {game_id} with {len(inserted)} documents")

    return game_id



#queries elastic search index for relevant text chunks
def query_elastic_search_by_index(es_client, index, user_question):    
    embeddings_model = embs.initialize_embeddings_model()    
    embedded_question = embeddings_model.embed_documents([user_question])[0]

    #dense vector search (essentially semantic search)
    response = es_client.search(
        index=index,
        knn={
            "field": "content_vector",
            "query_vector": embedded_question,
            "k": 10,
            "num_candidates": 1000
        },
    )

    # print("query results")
    # print(response)

    hits = response['hits']['hits']
    contexts = hits[0]['_source']['content']
    # contexts = []
    # for hit in hits: 
    #     context = hit['_source']['context']
    #     print(context)
    #     contexts.append(context)
    
    return contexts


#queries elastic search index for relevant text chunks
def query_elastic_search_by_index_bgg(es_client, index, user_question):    
    embeddings_model = embs.initialize_embeddings_model()    
    embedded_question = embeddings_model.embed_documents(user_question)[0]
    print(embedded_question)

    #dense vector search (essentially semantic search)
    response = es_client.search(
        index=index,
        knn={
            "field": "question_vector",
            "query_vector": embedded_question,
            "k": 10,
            "num_candidates": 1000
        }
    )

    print("query results")
    # print(response)

    hits = response['hits']['hits']
    contexts = hits[0]['_source']['question']
    
    # contexts = []
    for hit in hits: 
        print("ANSWER")
        context = hit['_source']['answer']
        print(context)
        print("QUESTION")
        context = hit['_source']['question']
        print(context)
       
    
    return contexts