from flask import Flask, request, jsonify
from flask_cors import CORS
from gpt import *
from loader import load_supported_games
import elastic_search as elastic_search
from werkzeug.utils import secure_filename
from requests import request as req
from json import dumps, loads
import constants as constants

app = Flask(__name__)
CORS(app)

es_client = elastic_search.get_client()
print(es_client.info())

#load games from "uploads/supported_games" into ElasticSearch
load_supported_games(es_client)

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
   userQuestion = request.args['prompt']
   #TODO front end needs to send selected game index 
   #index = request.args['index']
   index = 'index_20240323162803'
   print("User question:", userQuestion)

   #Query elastic search for matching game context
   contexts = elastic_search.query_elastic_search_by_index(es_client, index, userQuestion, hits=2)
   print("Response gathered from elasticsearch. Contexts:", contexts)

   #get answer from gpt api
   answer = get_completion_from_messages(contexts, userQuestion) 
   print("Response from GPT:", answer)

   answer = jsonify({'response': answer}) 
   answer.headers.add('Access-Control-Allow-Origin', '*')
   answer.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,PATCH,OPTIONS')
   
   #TODO, return actual answer!
   return jsonify({'response': 'answer'}) 



@app.route("/test", methods= ['GET'])
def test():
   index = elastic_search.new_game_index(es_client, 'server/uploads/root.pdf')
   return index


@app.route("/uploadPDF", methods= ['POST'])
def uploadPDF():
   if request.method == 'POST':
      file = request.files['the_file']
      print(f"User uploaded file: {secure_filename(file.filename)}")

      file.save(rf"uploads/{secure_filename(file.filename)}")

      index = elastic_search.new_game_index(es_client, rf'uploads/{secure_filename(file.filename)}')

      response = jsonify({"index": index})

      return response
   else:
      # TODO: Add error handling
      print('error')
     

#Returns a list of supported games and their indexes to the front end to be displayed on the sidebar
@app.route("/getSupportedGames", methods= ['GET'])
def getSupportedGames():
    supported_games = constants.supported_games
    #convert to json
    games_list = [{"name": game, "index": index} for game, index in supported_games]
    json_data = {"games": games_list}
    print(jsonify(json_data))
    return jsonify(json_data)


if __name__ == "__main__":
   app.run(debug=True, use_reloader=False)
