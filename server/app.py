from flask import Flask, request, jsonify
from flask_cors import CORS
from gpt import *
# import elastic_search as elastic_search
from werkzeug.utils import secure_filename


app = Flask(__name__)
CORS(app)

# es_client = elastic_search.get_client()
# print(es_client.info())

@app.route("/getAnswer", methods= ['POST'])
def getAnswer():
   if request.method == 'POST':
      print('get answer entered') 
      userQuestion = request.args.get('prompt')
      index = 'index_20240323020008'
      context = elastic_search.query_elastic_search_by_index(es_client, index, userQuestion)
      print("response gathered from elasticsearch")
      # print(context)
      finalResponse = get_completion_from_messages(context, userQuestion) 
      print("response from gpt:", finalResponse)
      answer = jsonify({'response': finalResponse}) 
      answer.headers.add('Access-Control-Allow-Origin', '*')
      print(answer)
      return answer
   else:
      print('error')

@app.route("/test", methods= ['GET'])
def test():
   index = elastic_search.new_game_index(es_client, 'server/root.pdf')
   return index

@app.route("/uploadPDF", methods= ['POST'])
def uploadPDF():
   if request.method == 'POST':
      file = request.files['the_file']

      print("here is the file we wan to save:", file)
      file.save(f"server/uploads/{secure_filename(file.filename)}")

      return 'upload pdf entered'
   else:
      print('error')
     

if __name__ == "__main__":
   app.run(debug=True)
