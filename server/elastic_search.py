import datetime

#ES
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk

#embeddings
import embs as embs

import pdf_parsing
import semantic_search
from mappings import mappings

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

def index_already_exists(es_client, index):
    return es_client.indices.exists(index=index)

def new_game_index(es_client, pdf_path, index=None):
    all_blocks = pdf_parsing.get_text_blocks_from_doc(pdf_path)
    print(f"Extracted {len(all_blocks)} text blocks from PDF file")
    consolidated_blocks = pdf_parsing.consolidate_broken_sentences(all_blocks)
    print(f"Consolidated into {len(consolidated_blocks)} blocks")
    semantic_blocks = semantic_search.group_by_semantic_similarity(consolidated_blocks)
    print(f"Grouped into {len(semantic_blocks)} semantic blocks")

    #if an index is specified in args, hardcode the index, otherwise, create new index using datetime
    if index is None:
        index = "index_" + datetime.datetime.now().strftime("%Y%m%d%H%M%S")

    mappings['_meta']['document_path'] = pdf_path

    try:
        es_client.indices.create(index=index, mappings=mappings)
    except Exception as e:
        raise Exception(f"Could not create new ElasticSearch index: {index}") 

    # Bulk insert the documents into the index
    operations = []
    for block in semantic_blocks:
        operations.append({"index": {"_index": index}})

        deconstructed_coordinates = []
        for quads in block['coordinates']:
            decon_quads = [pdf_parsing.quad_to_tuple(quad) for quad in quads]
            deconstructed_coordinates.append(decon_quads)

        doc_object = {
            "text": block['text'],
            "text_vector": block['full_text_embedding'],
            "page": block['page'],
            "page_block_index": block['index_on_page'],
            "page_coordinates": deconstructed_coordinates
        }
        operations.append(doc_object)
    response = es_client.bulk(index=index, operations=operations, refresh=True)

    inserted = response["items"]
    print(f"Created index {index} with {len(inserted)} documents")

    return index


#queries elastic search index for relevant text chunks
def query_elastic_search_by_index(es_client, index, user_question, hits=3):    
    embeddings_model = embs.get_embeddings()    
    embedded_question = embeddings_model.embed_query(user_question)

    #dense vector search (essentially semantic search)
    response = es_client.search(
        index=index,
        knn={
            "field": "text_vector",
            "query_vector": embedded_question,
            "k": hits,
            "num_candidates": 10000,
        },
    )

    hits = response['hits']['hits']
    blocks = []
    for hit in hits:
        block = {
            'confidence': hit['_score'],
        }
        for key in hit['_source'].keys():
            if key == 'text_vector':
                continue
            block[key] = hit['_source'][key]

        coordinates = []

        for decon_quads in block['page_coordinates']:
            quads = [pdf_parsing.tuple_to_quad(tuple) for tuple in decon_quads]
            coordinates.append(quads)

        block['coordinates'] = coordinates
        blocks.append(block)
    
    return blocks