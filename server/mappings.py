# structure of elasticsearch indices
mappings = {
    "_meta": {
        "document_path": ""
    },
    "properties": {
        "text": {
            "type": "text"
        },
        "text_vector": {
            "type": "dense_vector",
            "dims": 384,
            "index": "true",
            "similarity": "cosine"
        },
        "page": {
            "type": "integer"
        },
        "page_block_index": {
            "type": "integer"
        },
        "page_coordinates": {
            "type": "object",
            "enabled": False
        }

    }
}