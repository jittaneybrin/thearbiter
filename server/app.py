from flask import Flask, request, jsonify
from flask_cors import CORS
from gpt import *
import elastic_search as elastic_search
from werkzeug.utils import secure_filename
from requests import request as req
from json import dumps, loads


app = Flask(__name__)
CORS(app)


appId = 't4KsGHvY'
talkJSSecretKey = 'sk_test_hr35P6vuhJ5x7UVN8jqv3wB3WLIUX5DB'
basePath = "https://api.talkjs.com"
conversationId = "sample_conversation"

# es_client = elastic_search.get_client()
# print(es_client.info())

# TODO: Rearrange the organization of the code
def getResponse(json): 
    del json['createdAt']
    userQuestion = json['data']['message']['text']
    index = 'index_20240323162803'
    context = elastic_search.query_elastic_search_by_index(es_client, index, userQuestion)
    print("response gathered from elasticsearch")
    answer = get_completion_from_messages(context, userQuestion) 
    print("response from gpt api")
    return answer 



@app.route("/getAnswer", methods= ['POST'])
def getAnswer():
    print('get answer entered') 
    if request.method == 'POST':
      answer = jsonify({'response': 'test answer'}) 
      answer.headers.add('Access-Control-Allow-Origin', '*')
      answer.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,PATCH,OPTIONS')

      return answer
    else:
      # TODO: Add error handling
      print('error')



@app.route("/test", methods= ['GET'])
def test():
   index = elastic_search.new_game_index(es_client, 'server/uploads/root.pdf')
   return index

@app.route("/uploadPDF", methods= ['POST'])
def uploadPDF():
   if request.method == 'POST':
      file = request.files['the_file']
      print(f"User uploaded file: {secure_filename(file.filename)}")

      file.save(f"server/uploads/{secure_filename(file.filename)}")

      index = elastic_search.new_game_index(es_client, f'server/uploads/{secure_filename(file.filename)}')

      response = jsonify({"index": index})

      return response
   else:
      # TODO: Add error handling
      print('error')
     

if __name__ == "__main__":
   app.run(debug=True, use_reloader=False)
