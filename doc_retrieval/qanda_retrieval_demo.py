import server.settings as settings

#for html requests and html parsing
import requests
from bs4 import BeautifulSoup

#ES
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk

#for embedding text
from langchain_community.vectorstores import FAISS
import langchain.schema.document as d
from langchain_community.embeddings import HuggingFaceEmbeddings

import datetime

TEXT_CHUNK_SIZE = 500
CHUNK_OVERLAP_SIZE = 100

client = Elasticsearch(
    "https://localhost:9200",
    ssl_assert_fingerprint = settings.CERT_FINGERPRINT,
    basic_auth=("elastic", settings.ELASTIC_PASSWORD)
)

# Grab wikipedia html content from source url
def get_wikipedia_page(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        print(f"Error: could not get page: {url}")
        return None

# Parse paragraphs (text) and title from the Wikipedia page
def extract_paragraphs_and_title(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    paragraphs = []
    for p in soup.find_all('p'):
        paragraphs.append(p.get_text())
    for title in soup.find_all('title'):
        T = title.get_text()
    return paragraphs, T

#remove \n's from paragraphs
def split_paragraphs(paragraphs):
    new_paragraphs = []
    for p in paragraphs:
        split_paragraphs = p.split('\n')
        for text in split_paragraphs:
            if text != " " and text != "":
                new_paragraphs.append(text)
    return new_paragraphs

#chunk paragraphs into chunks of {chunk_size} with overlap of {overlap_size}
def chunk_paragraph(paragraph, chunk_size, overlap_size):
    chunks = []
    text_remaining = paragraph
    while len(text_remaining) > 0:
        if len(text_remaining) <= chunk_size:
            chunks.append(text_remaining)
            text_remaining = ""
        else:
            chunks.append(text_remaining[0:chunk_size])
            text_remaining = text_remaining[chunk_size-overlap_size:]
    return chunks


# URL of the Wikipedia page
url = 'https://en.wikipedia.org/wiki/Abraham_Lincoln'

# Get the Wikipedia page
html_content = get_wikipedia_page(url)

# Extract paragraphs from the Wikipedia page
paragraphs, title = extract_paragraphs_and_title(html_content)
paragraphs = split_paragraphs(paragraphs)
chunks = paragraphs 

#split up large paragraphs into chunks to keep pieces of text smaller
# chunks = []
# for p in paragraphs:
#     chunks.extend(chunk_paragraph(p, TEXT_CHUNK_SIZE, CHUNK_OVERLAP_SIZE))

def initialize_embeddings_model():
    # Define the path to the pre-trained model you want to use
    modelPath = "sentence-transformers/all-MiniLM-l6-v2"

    # Create a dictionary with model configuration options, specifying to use the CPU for computations
    model_kwargs = {'device': 'cpu'}

    # Create a dictionary with encoding options, specifically setting 'normalize_embeddings' to False
    encode_kwargs = {'normalize_embeddings': False}

    # Initialize an instance of HuggingFaceEmbeddings with the specified parameters
    embeddings = HuggingFaceEmbeddings(
        model_name=modelPath,     # Provide the pre-trained model's path
        model_kwargs=model_kwargs, # Pass the model configuration options
        encode_kwargs=encode_kwargs # Pass the encoding options
    )
    return embeddings

#create documents for Faiss
metadata = {
    'source': url, 
    'title': title,
    'date_time': datetime.datetime.now()
}
docs_for_faiss = []
for chunk in chunks:
    docs_for_faiss.append(d.Document(page_content=chunk, metadata=metadata))

#Set up text embedding model:
embeddings_model = initialize_embeddings_model()
#load documents into FAISS vector database
db = FAISS.from_documents(docs_for_faiss, embeddings_model)

#Q and A Session
while True:
    user_question = input("Ask a question about Abraham Lincoln: \n\n")
    #Grab the relevant material using FAISS
    searchDocs = db.similarity_search(user_question)
    #print the two most relevant pieces of text:
    print("\nBelow are the two most relevant answers using FAISS vector search: ")
    print("\nTEXT 1:")
    print(searchDocs[0].page_content)
    print("\nTEXT 2:")
    print(searchDocs[1].page_content)

    #Grab the relevant material using Elasticsearch
    query = {
        "query": {
            "match": {
            "text": {
                "query": user_question,
                "minimum_should_match": "10%"
            }
            }
        }}

    index = 'abe2'
    response = client.search(index=index, body=query)
    #print the two most relevant pieces of text:
    num_results = len(response["hits"]["hits"])
    if num_results == 0:
        print("\nElasticsearch did not return any results.\n")
    else:
        print("\nBelow are the two most relevant answers using ElasticSearch: \n")
        print("\nTEXT 1:")
        print(response["hits"]["hits"][0])
        if num_results > 1:
            print("\nTEXT 2:")
            print(response["hits"]["hits"][1])
    print('\n')




    
