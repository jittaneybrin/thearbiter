from flask import Flask, request, render_template, jsonify
from openai import OpenAI
from settings import API_KEY

client = OpenAI(
    api_key = API_KEY
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
        "content": prompt[0]
        }
        ],
        model="gpt-3.5-turbo",
        max_tokens=10
    )
    return chat_completion.choices[0].message.content



