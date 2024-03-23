from flask import Flask, request, render_template, jsonify
from openai import OpenAI
from settings import API_KEY

client = OpenAI(
    api_key = API_KEY
)

def get_completion_from_messages(context, question):
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": "With the following context: \"" + context + "\" answer the following question: \"" + question + "\""
                },
        ],
        model="gpt-3.5-turbo",
        max_tokens=10
    )
    # print(chat_completion)
    return chat_completion.choices[0].message.content



