## Folder Structure

- server
    - app.py :  The main Flask server code file.
    - chatbot.py : The file containing the logic for the chatbot.
    - vectordb : Contains files related to the indexing of data.
    - data : Contains the data sheets for project.
    - requirements.txt : Includes all project dependencies.
    - README.md


## Setting Up Flask Environment

1. In app.py, we can set different parameters while initializing the chatbot object (line number 17).
        
    ##### Following are the default values.
        
        debug = True # adds user id, cost, tokens, time used for each request.
        k = 5 # finds top 5 similar documents
        verbose = True # prints standalone question, context used for each request in console.
        model_name = 'text-davinci-003'

2. Make sure you have Python 3.8.10 or higher

3. Create a Python virtual environment of name server

        python3 -m venv server

4. Activate the virtual environment using one of following command

        source venv/bin/activate 
        . venv/bin/activate

5. Install the required libraries

        pip install -r requirements.txt

6. create a .env file in same directory and add API keys in it as follows

    To create .env file you can use in linux

        touch .env

    Inside .env file

        MY_API_KEY=[OpenAi API key]
        X_API_KEY=[API key for client-server communication]