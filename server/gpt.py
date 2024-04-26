from flask import Flask, request, render_template, jsonify
from openai import OpenAI
from settings import API_KEY

client = OpenAI(
    api_key = API_KEY
)

def get_completion_from_messages(contexts, question):

    content = "With the following context: \n"
    for index, context in enumerate(contexts):
        content += f"context {index+1}: \"{context['text']}\"\n"
    content += f"Answer the following question as concisely, yet professional as possible: \"{question}\" ."

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": content
                },
        ],
        model="gpt-3.5-turbo",
        max_tokens=100
    )
    # print(chat_completion)
    return chat_completion.choices[0].message.content



