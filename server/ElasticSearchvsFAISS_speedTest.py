from elastic_search import *
from gpt import *
import time
import loader as loader
import embs as embs
from langchain_community.vectorstores import FAISS
import langchain.schema.document as d

#Speed comparison between Fiass vector retrieval and Elastic Search Vector retrieval

es_client = get_client()

def test(faiss_db):
    userQuestion = "How do I perform a castle?"

    #hard coded chess index
    index = 'chess_supported_index'
    
    start_time_es = time.time()
    context = query_elastic_search_by_index(es_client, index, userQuestion)
    end_time_es = time.time()
    print("Time taken by ElasticSearch function:", end_time_es - start_time_es, "seconds")
    print("response gathered from elasticsearch")

    start_time_es = time.time()
    searchDocs = faiss_db.similarity_search(userQuestion,3)
    #print the two most relevant pieces of text:loader
    end_time_es = time.time()
    print("Time taken by Faiss:", end_time_es - start_time_es, "seconds")
    print("response gathered from Faiss")

    # print("\nBelow is the most relevant answer using FAISS vector search: ")
    # print("\nTEXT 1:")
    # #print(searchDocs[0].page_content)

def get_faiss_db(pdf_path):
    reader = PdfReader(pdf_path)

    pdf_content = ""
    for page in reader.pages:
        text = page.extract_text()
        pdf_content += text

    text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
        chunk_size=512, chunk_overlap=256
    )
    docs = text_splitter.create_documents([pdf_content])

    paragraphs = loader.get_chess_paragraphs()
    #create documents for Faiss
    metadata = {
        'date_time': datetime.datetime.now()
    }

    docs_for_faiss = []
    for doc in docs:
        docs_for_faiss.append(d.Document(page_content=doc.page_content, metadata=metadata))

    #Set up text embedding model:
    embeddings_model = embs.initialize_embeddings_model()
    #load documents into FAISS vector database
    db = FAISS.from_documents(docs_for_faiss, embeddings_model)
    return db


path = rf'server/uploads/supported_games/chess.pdf'
chess_faiss_db = get_faiss_db(path)
test(chess_faiss_db)