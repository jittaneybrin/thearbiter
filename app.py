from flask import Flask, request, render_template, jsonify
from elasticsearch import Elasticsearch
from openai import OpenAI

app = Flask(__name__)

ELASTIC_PASSWORD = "06Tv9FUtTxQ43sdNuSdU"
CERT_FINGERPRINT = "e01bcdaa455cbab53bd08776aa99a3263fd8fa6c8b18d933972e936408869d09"
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
        "content": "You are a helpful assistant."
        },
        {
        "role": "user",
        "content": prompt
        }
        ],
        model="gpt-3.5-turbo",
        max_tokens=100
    )
    return chat_completion.choices[0].message.content


@app.route("/")
def home():
    return render_template("index.html")

@app.route("/gptapi", methods=['GET', 'POST'])
def gptai():
    print("hi")
    if request.method == 'POST': 
        print('POST entered') 
        prompt = request.form['prompt'] 
        response = get_completion_from_messages(prompt) 
        return jsonify({'response': response}) 
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
