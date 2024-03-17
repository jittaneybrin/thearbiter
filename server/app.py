from flask import Flask, request, render_template, jsonify
from flask_cors import CORS
from elasticsearch import Elasticsearch
from openai import OpenAI


app = Flask(__name__)
CORS(app)

ELASTIC_PASSWORD = "-2A0m7xn4sDU*1gdBpKR"
CERT_FINGERPRINT = "cbb3569b3161deaa711343e4d703d281df69d8107718180dd3d290a6fd848c82"
MAX_SIZE = 15

es = Elasticsearch(
    "https://localhost:9200",
    ssl_assert_fingerprint=CERT_FINGERPRINT,
    basic_auth=("elastic", ELASTIC_PASSWORD)
)

client = OpenAI(
    api_key="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"
)

def get_completion_from_messages(prompt):
    
    chat_completion = client.chat.completions.create(
        messages=[
            {
        "role": "system",
        "content": "You are a master of playing board games. Your job is to rephrase a paragraph that in a tone that is friendly, helpful, bubbly, and human-like."
        },
        {
        "role": "user",
        "content": "Stalemate is a situation in chess where the player whose turn it is to move is not in check and has no legal move. Stalemate results in a draw. During the endgame, stalemate is a resource that can enable the player with the inferior position to draw the game rather than lose. In more complex positions, stalemate is much rarer, usually taking the form of a swindle that succeeds only if the superior side is inattentive. Stalemate is also a common theme in endgame studies and other chess problems."
        }
        ],
        model="gpt-3.5-turbo",
        max_tokens=10
    )
    return chat_completion.choices[0].message.content


@app.route("/")
def home():
    return "hi"

@app.route("/gptapi", methods=['GET', 'POST'])
def gptai():
    print("hi")
    print(request)
    if request.method == 'POST': 
        print('POST entered') 
        prompt = ''
        response = get_completion_from_messages(prompt) 
        answer = jsonify({'response': response}) 
        answer.headers.add('Access-Control-Allow-Origin', '*')
        print(answer)
        return answer
    return render_template('gptapi.html')

# @app.route("/search")
# def search_autocomplete():
#     query = request.args["q"].lower()
#     tokens = query.split(" ")

#     clauses = [
#         {
#             "span_multi": {
#                 "match": {"fuzzy": {"name": {"value": i, "fuzziness": "AUTO"}}}
#             }
#         }
#         for i in tokens
#     ]

#     payload = {
#         "bool": {
#             "must": [{"span_near": {"clauses": clauses, "slop": 0, "in_order": False}}]
#         }
#     }

#     resp = es.search(index="cars", query=payload, size=MAX_SIZE)
#     for result in resp['hits']['hits']:
#         print(result['_source']['name'])
#     return [result['_source']['name'] for result in resp['hits']['hits']]


if __name__ == "__main__":
    app.run(debug=True)
