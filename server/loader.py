
import settings as settings
from elasticsearch import Elasticsearch

#for html requests and html parsing
import requests
from bs4 import BeautifulSoup

#ES
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk

import elastic_search as elastic_search 

TEXT_CHUNK_SIZE = 500
CHUNK_OVERLAP_SIZE = 100

MAX_SIZE = 15

# URL of the Wikipedia page
abe_url = 'https://en.wikipedia.org/wiki/Abraham_Lincoln'
chess_url = 'https://en.wikipedia.org/wiki/Rules_of_chess'

client = Elasticsearch(
    "https://localhost:9200",
    ssl_assert_fingerprint = settings.CERT_FINGERPRINT,
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

def load_chess():
    # Get the Wikipedia page
    html_content = get_wikipedia_page(chess_url)

    # Extract paragraphs from the Wikipedia page
    paragraphs, title = extract_paragraphs_and_title(html_content)

    paragraphs = split_paragraphs(paragraphs)

    index = "chess_index10"
    game = "Chess"
    try:
        elastic_search.new_game_index(client, index, game, paragraphs)
        print(f"Done Loading {game} into ElasticSearch")
    except Exception as e:
        print(f"Could not create the {game} index. Exception: {e}")

# load_chess()
# print(elastic_search.query_elastic_search_by_index(client, "chess_index10", "what is a stalemate"))

