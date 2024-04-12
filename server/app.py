from flask import Flask, request, jsonify
from flask_cors import CORS
from gpt import *
from loader import load_supported_games
import elastic_search as elastic_search
from werkzeug.utils import secure_filename
import constants as constants

app = Flask(__name__)
CORS(app)

#Start up code
es_client = elastic_search.get_client()
load_supported_games(es_client)

#Gathers user question and corresponding game from front end, queries ElasticSearch for context, then GPT for an answer
#and returns the answer
@app.route("/getAnswer", methods= ['POST'])
def getAnswer():
   userQuestion = request.args['prompt']
   #TODO front end needs to send selected game index 
   index = request.args['index']
   #index = 'index_20240323162803'
   print("user index:", index)
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
   
   return answer

#Handles PDF upload from the front end, returns newly created ElasticSearch index
@app.route("/uploadPDF", methods= ['POST'])
def uploadPDF():
   file = request.files['the_file']
   print(f"User uploaded file: {secure_filename(file.filename)}")
   file.save(rf"uploads/{secure_filename(file.filename)}")

   #load file into ElasticSearch, save the new index
   index = elastic_search.new_game_index(es_client, rf'uploads/{secure_filename(file.filename)}')
   response = jsonify({"index": index})
   
   return response
     

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
