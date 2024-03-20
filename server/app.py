from flask import Flask, request, render_template, jsonify
from flask_cors import CORS
from elasticsearch import Elasticsearch
from openai import OpenAI
from settings import CERT_FINGERPRINT, ELASTIC_PASSWORD
from gpt import *
from elastic_search import *

app = Flask(__name__)
CORS(app)

es_client = Elasticsearch(
    "https://127.0.0.1:9200",
    ssl_assert_fingerprint = CERT_FINGERPRINT,
    basic_auth=("elastic", ELASTIC_PASSWORD)
)


@app.route("/getAnswer", methods= ['POST'])
def getAnswer():
     if request.method == 'POST': 
        print('get answer entered') 
        userQuestion = request.args.get('prompt')
        index = 'chess_index10'
        response = query_elastic_search_by_index(es_client, index, userQuestion)
        finalResponse = get_completion_from_messages(response) 
        answer = jsonify({'response': finalResponse}) 
        answer.headers.add('Access-Control-Allow-Origin', '*')
        print(answer)
        return answer
     else:
        print('error')
     

if __name__ == "__main__":
    app.run(debug=True)
