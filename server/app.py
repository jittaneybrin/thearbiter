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

es_client = elastic_search.get_client()
print(es_client.info())

@app.route("/getAnswer", methods= ['POST'])
def getAnswer():
    print('get answer entered') 
    if request.method == 'POST':
      del request.json['createdAt']
      userQuestion = request.json['data']['message']['text']
      print(userQuestion)
      index = 'index_20240323162803'
      context = elastic_search.query_elastic_search_by_index(es_client, index, userQuestion)
      print("response gathered from elasticsearch")
      answer = get_completion_from_messages(context, userQuestion) 
      print("gpt api")

      url = "https://api.talkjs.com/v1/t4KsGHvY/conversations/sample_conversation/messages"

      payload = dumps([
        {
          "text": answer,
          "type": "UserMessage",
          "sender": "sample_user_sebastian"
        }
      ])
      headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer sk_test_hr35P6vuhJ5x7UVN8jqv3wB3WLIUX5DB'
      }

      response = req("POST", url, headers=headers, data=payload)
      print(response.text)
      return response.text
    else:
      print('error')

@app.route("/test", methods= ['GET'])
def test():
   index = elastic_search.new_game_index(es_client, 'server/root.pdf')
   return index

@app.route("/uploadPDF", methods= ['POST'])
def uploadPDF():
   if request.method == 'POST':
      print('upload pdf entered')
      # file = request.files['the_file']
      # file.save(f"/server/uploads/{secure_filename(file.filename)}")

      return 'upload pdf entered'
   else:
      print('error')
     

if __name__ == "__main__":
   app.run(debug=True)
