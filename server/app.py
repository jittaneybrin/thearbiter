from flask import Flask, request, jsonify
from flask_cors import CORS
from gpt import *
import elastic_search as elastic_search
from werkzeug.utils import secure_filename
from requests import request as req
from json import dumps, loads
from xmltodict import parse
from html.parser import HTMLParser
from math import ceil




app = Flask(__name__)
CORS(app)


appId = 't4KsGHvY'
talkJSSecretKey = 'sk_test_hr35P6vuhJ5x7UVN8jqv3wB3WLIUX5DB'
basePath = "https://api.talkjs.com"
conversationId = "sample_conversation"

es_client = elastic_search.get_client()
print(es_client.info())

def bggapi(gameId):
  url = "https://boardgamegeek.com/xmlapi2/forumlist?id="+str(gameId)+"&type=thing"
  response = req("GET", url)
  forumListJsonObject = parse(response.content)
  listOfForums = forumListJsonObject["forums"]["forum"]
  listOfForumIds = []
  for forum in listOfForums:
    if forum["@title"] == "Rules":
       listOfForumIds.append(forum["@id"])
  print("forumid = ", listOfForumIds)
  listOfThreadIds = []
  for id in listOfForumIds:
    print(id)
    url = "https://boardgamegeek.com/xmlapi2/forum?id="+str(id)
    response = req("GET", url)
    forumJson = parse(response.content)
    numOfThreads = int(forumJson["forum"]["@numthreads"])
    print(numOfThreads)
    print(ceil(numOfThreads/50))
    
    for i in range(ceil(numOfThreads/50)):
      url = "https://boardgamegeek.com/xmlapi2/forum?id="+str(id)+"&page="+str(i)
      response = req("GET", url)
      forumJson = parse(response.content)
      for thread in forumJson["forum"]["threads"]["thread"]:
        listOfThreadIds.append(thread["@id"])
    
  print(listOfThreadIds)
  listOfQuestions = []
  listOfAnswers = []

  for id in listOfThreadIds:
    url = "https://boardgamegeek.com/xmlapi2/thread?id="+str(id)
    response = req("GET", url)
    threadJson = parse(response.content)
    if threadJson.get("thread"):
      print(type(threadJson["thread"]["articles"]["article"]))
      if type(threadJson["thread"]["articles"]["article"]) is list:
        if(threadJson["thread"]["articles"]["article"][0].get("body")):
          listOfQuestions.append(threadJson["thread"]["articles"]["article"][0]["body"])
        else:
          listOfQuestions.append("null")
        if(threadJson["thread"]["articles"]["article"][1].get("body")):
          listOfAnswers.append(threadJson["thread"]["articles"]["article"][1]["body"])
        else:
          listOfAnswers.append("null")
  print(len(listOfAnswers))
  print(len(listOfQuestions))
  return listOfAnswers, listOfQuestions

# TODO: Rearrange the organization of the code
def getResponse(json): 
    del json['createdAt']
    userQuestion = json['data']['message']['text']
    index = 'index_20240323162803'
    context = elastic_search.query_elastic_search_by_index(es_client, index, userQuestion)
    game_id = 13
    forum_context = elastic_search.query_elastic_search_by_index_bgg(es_client, game_id, userQuestion)
    print(context)
    print("response gathered from elasticsearch")
    answer = get_completion_from_messages(context, userQuestion) 
    print("response from gpt api")

    url = "https://api.talkjs.com/v1/t4KsGHvY/conversations/sample_conversation/messages"
    payload = dumps([
      {
        "text": answer + '\n' + forum_context,
        "type": "UserMessage",
        "sender": "sample_user_sebastian", 
        "idempotencyKey": json['data']['message']['id']
      }
    ])
    headers = {
      'Content-Type': 'application/json',
      'Authorization': 'Bearer sk_test_hr35P6vuhJ5x7UVN8jqv3wB3WLIUX5DB'
    }

    req("POST", url, headers=headers, data=payload)


@app.route("/getAnswer", methods= ['POST'])
def getAnswer():
    print('get answer entered') 
    if request.method == 'POST':
      if request.json['data']['message']['senderId'] == 'sample_user_alice':   
        getResponse(request.json)
      return '', 200
    else:
      # TODO: Add error handling
      print('error')

@app.route("/test", methods= ['GET'])
def test():
   index = elastic_search.new_game_index(es_client, 'server/uploads/root.pdf')
   return index


@app.route("/testbggelasticsearch", methods = ['GET'])
def testbggelasticsearch():
    if request.method == 'GET':
      id = 13
      listOfAnswers, listOfQuestions = bggapi(id)
      elastic_search.new_forum(es_client, listOfQuestions, listOfAnswers, id)    
    return "done"   

@app.route("/testbggquery", methods = ['GET'])
def testbggquery():
    if request.method == 'GET':
      id = 171
      question = "can the vagabond give aid to the lord of the hundreds and take an item from the hoard?"
      elastic_search.query_elastic_search_by_index_bgg(es_client, id, question)
    return "done"   

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
