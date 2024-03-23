# The Arbiter
Board game question answerer

## Group members:
- Adam Saleh
- Brittaney Jin
- Matt LeHoty
- Jake Sutter
- Samridhi Kaushik


# Project Setup
## Installation
1. Create a python virtual environment
    ```shell
    python -m venv .venv
    ```
2. Activate virtual environment

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

3. Install Python packages
    ```shell
    pip install -r requirement.txt
    ```
4. Install node modules
    
    From within the client folder: 
    ```shell
    npm install
    ```
5. Update Elasticsearch password and certification fingerprint in server/settings.py
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

# Todo
- [ ] Document Elasticsearch docker container configuring
- [ ] Add frontend POST call to server's /uploadPDF

# Current Notes
- game index is hardcoded in server/app.py route