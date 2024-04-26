# The Arbiter
Retrieval-agumented generation (RAG) board game chatbot

## Group members:
- Adam Saleh
- Brittaney Jin
- Matt LeHoty
- Jake Sutter
- Samridhi Kaushik

# Notes
- The GPT API connection has been disabled. You either need to get your own (and populate the key in settings.py) or find a new method and update the functionality in /server/gpt.py. I do think it needs to be the same gpt-3.5-turbo model if you want it to work immediately. Otherwise, it's probably another small update in the gpt.py file.

# Project Setup
## Installation
1. [Create an Elasticsearch container via Docker](https://www.elastic.co/guide/en/elasticsearch/reference/current/docker.html)
2. Create a python virtual environment
    ```shell
    python -m venv .venv
    ```
3. Activate virtual environment

    If you're using Windows CMD:
    ```
    .\.venv\Scripts\activate.bat
    ```
    If you're using Windows Powershell:
    ```
    .\.venv\Scripts\Activate.ps1
    ```
    If you're using Unix or MacOS:
    ```shell
    source .venv/bin/activate
    ```

4. Install Python packages
    ```shell
    pip install -r requirements.txt
    ```
5. Install node modules
    
    From within the client folder: 
    ```shell
    npm install
    ```
6. Update Elasticsearch password and certification fingerprint in server/settings.py
## Starting Servers
1. Start Elasticsearch docker container
2. Start the React server

    In a terminal within the client folder, run:
    ```shell
    npm start
    ```
    As displayed in the logs
    > To create a production build, use `npm run build`.
    
    Thus, `building` is not necessary for development purposes.

3. Start the Flask app
    
    In a new terminal session, run:
    ```shell
    flask --app .\server\app.py run
    ```
## Open App
By default, you should be able to view the website at [http://localhost:3000](http://localhost:300)