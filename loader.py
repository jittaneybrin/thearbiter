
import settings
from elasticsearch import Elasticsearch
#for html requests and html parsing
import requests
from bs4 import BeautifulSoup

#ES
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
import datetime

TEXT_CHUNK_SIZE = 500
CHUNK_OVERLAP_SIZE = 100

kibana = 'eyJ2ZXIiOiI4LjEyLjEiLCJhZHIiOlsiMTcyLjE4LjAuMjo5MjAwIl0sImZnciI6ImUwMWJjZGFhNDU1Y2JhYjUzYmQwODc3NmFhOTlhMzI2M2ZkOGZhNmM4YjE4ZDkzMzk3MmU5MzY0MDg4NjlkMDkiLCJrZXkiOiJ6N0VadlkwQk5neUVfUTd1OXZmNDpZN2o3M2duQ1N1Q3NjRXd0V3JMbjR3In0='
MAX_SIZE = 15


# URL of the Wikipedia page
url = 'https://en.wikipedia.org/wiki/Abraham_Lincoln'


client = Elasticsearch(
    "https://localhost:9200",
    ssl_assert_fingerprint= settings.CERT_FINGERPRINT,
    basic_auth=("elastic", settings.ELASTIC_PASSWORD)
)

print(f"Connected to ElasticSearch cluster `{client.info().body['cluster_name']}`")
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




# Get the Wikipedia page
html_content = get_wikipedia_page(url)
# Extract paragraphs from the Wikipedia page
paragraphs, title = extract_paragraphs_and_title(html_content)

paragraphs = split_paragraphs(paragraphs)
chunks = paragraphs 

#create documents for ElasticSearch
docs_for_elasticsearch = []
for chunk in chunks:
    docs_for_elasticsearch.append(
        {
        '_index': 'abe2',
        '_source': {
            'game': 'abe',
            'text': chunk,
            'timestamp': datetime.datetime.now()
        }})
    
#load documents into ElasticSearch
#ONLY DO THIS ONCE!!
response = bulk(client, docs_for_elasticsearch)
