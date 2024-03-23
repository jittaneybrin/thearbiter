from flask import Flask, request, render_template, jsonify
from flask_cors import CORS
from elasticsearch import Elasticsearch
from openai import OpenAI
from settings import CERT_FINGERPRINT, ELASTIC_PASSWORD
from gpt import *
import elastic_search as elastic_search

app = Flask(__name__)
CORS(app)

es_client = elastic_search.get_client()

@app.route("/getAnswer", methods= ['POST'])
def getAnswer():
     if request.method == 'POST': 
        print('get answer entered') 
        userQuestion = request.args.get('prompt')
        index = 'chess_index10'
        response = elastic_search.query_elastic_search_by_index(es_client, index, userQuestion)
        print("response gathered from elasticsearch")
        finalResponse = get_completion_from_messages(response) 
        print("response from gpt:", finalResponse)
        answer = jsonify({'response': finalResponse}) 
        answer.headers.add('Access-Control-Allow-Origin', '*')
        print(answer)
        return answer
     else:
        print('error')
     

if __name__ == "__main__":
    app.run(debug=True)
