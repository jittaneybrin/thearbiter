
import settings as settings
import elastic_search as elastic_search 
from elasticsearch.helpers import bulk
import embs as embs
import datetime
import requests
from bs4 import BeautifulSoup

TEXT_CHUNK_SIZE = 500
CHUNK_OVERLAP_SIZE = 100
MAX_SIZE = 15

# URL of the Wikipedia page
abe_url = 'https://en.wikipedia.org/wiki/Abraham_Lincoln'
chess_url = 'https://en.wikipedia.org/wiki/Rules_of_chess'

client = elastic_search.get_client()

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

def new_game_index2(es_client, index, paragraphs):
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
    for p  in paragraphs:
        operations.append({"index": {"_index": index}})
        doc_object = {
            "content": p,
            # Transforming the title into an embedding using the model
            "content_vector": embeddings_model.embed_documents([p])[0]
        }
        operations.append(doc_object)
    response = es_client.bulk(index=index, operations=operations, refresh=True)
    inserted = response["items"]
    print(f"Created index {index} with {len(inserted)} documents")

    return index


def get_chess_paragraphs():
    # Get the Wikipedia page
    html_content = get_wikipedia_page(chess_url)

    # Extract paragraphs from the Wikipedia page
    paragraphs, title = extract_paragraphs_and_title(html_content)

    paragraphs = split_paragraphs(paragraphs)
    return paragraphs

def load_chess():
    # Get the Wikipedia page
    html_content = get_wikipedia_page(chess_url)

    # Extract paragraphs from the Wikipedia page
    paragraphs, title = extract_paragraphs_and_title(html_content)

    paragraphs = split_paragraphs(paragraphs)

    index = "chess_index110"
    game = "chess"
    try:
        new_game_index2(client, index, paragraphs)
        print(f"Done Loading {game} into ElasticSearch")
    except Exception as e:
        print(f"Could not create the {game} index. Exception: {e}")

def load_supported_games():
    print("in load supported games")
    supported_games = ["catan", "chess"]
    for game in supported_games:
        filedir = rf"uploads/supported_games/{game}.pdf"
        try:
            elastic_search.new_game_index(client, filedir, index=game)
            print(f"Successfully created new Elastic Search index for supported game: {game}")
        except Exception as e:
            print(f"Error: Could not create new Elastic Search index for supported game: {game}. Exception: {e}")
