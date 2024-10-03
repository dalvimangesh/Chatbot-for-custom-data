from flask import Flask, jsonify, request, abort
from chatbot import ChatBot
from flask_apscheduler import APScheduler
from time import time
from flask_cors import CORS
from uuid import uuid4
from functools import wraps
from dotenv import load_dotenv
import os
import logging

app = Flask(__name__)

try:
    # top k documents sending to OpenAi
    # default model_name = 'text-davinci-003'
    chatBot = ChatBot(debug=True, k=10, verbose = True)
except:
    print('Error in initializing ChatBot object')
    exit(-1)

chatHistory = dict()
chatTime = dict()
scheduler = APScheduler()
inactiveTimeLimit = 600
intervalTime = 60
load_dotenv()

# Access restricted
CORS(app=app, origins=['http://localhost:3000'])

'''
middleware function to validate the incoming request
'''
def require_appkey(view_function):

    @wraps(view_function)
    def decorated_function(*args, **kwargs): # the new, post-decoration function. Note *args and **kwargs here.

        if 'X-API-KEY' in request.headers and request.headers['X-API-KEY'] == os.getenv('X_API_KEY'):

            return view_function(*args, **kwargs)
        
        else:

            abort(401)

    return decorated_function


'''
In interval of intervalTime checking each user activity status
and if user is inactive for more than inactiveTimeLimit then
clearing the complete context of the same user
'''
@scheduler.task('interval', id='remove_inactive_user', seconds=intervalTime, misfire_grace_time=900)
def checkInactiveUsers():

    currentTime = time()

    ids = list(chatTime.keys())

    for _id in ids:

        inactiveTime = currentTime - chatTime[_id]

        if inactiveTime >= inactiveTimeLimit:

            # _id must always be present in chatTime and chatHistory

            del chatTime[_id]
            del chatHistory[_id]


'''
end point to get unique id using uuid4
'''
@app.route('/generate', methods=["GET"])
@require_appkey
def generate():

    uniqueUserId: str = str(uuid4())

    return jsonify(
        {
            "userId": uniqueUserId
        }
    )


'''
post request should be json in format 
{
    "id": ...unique_id... ,
    "question": ...question...
}
'''
@app.route('/chat', methods=["POST"])
@require_appkey
def chat():

    userQuery = request.json

    _id, _question = userQuery['id'], userQuery['question']

    if (_question == ''):  # first making connection with empty input

        chatHistory[_id] = list() # empty chat list for user
        chatTime[_id] = time() # session started

        return jsonify(
            {
                "answer": "Hello, How can I help you ?"
            }
        )

    if _id not in chatHistory: # checking session has expired or not
        abort(403)

    try:

        response  = chatBot.response(
            query={
                'question': _question,
                'chat_history': chatHistory[_id]
            },
            id=_id
        )

    except: # sending internal server error as openai is not working

        chatTime[_id] = time()
        abort(500) 

    tempResponse = response.strip().lower()

    if "don't" in tempResponse and 'know' in tempResponse: # if bot dont have any answer

        chatHistory[_id].append((_question, response)) # adding to maintain context
        response = "Hmm... 🤔🔍I'm sorry, but I don't have the answer to that question at the moment. Let's try something else! Feel free to ask me question on Genomic Wellness."
    
    else:

        chatHistory[_id].append((_question, response))  # storing chat history

    chatTime[_id] = time()  # setting last active time for current user

    return jsonify(
        {
            "answer": response
        }
    )


if __name__ == '__main__':

    scheduler.start()
    
    # Disable Flask logger
    app.logger.disabled = True

    # Disable all loggers
    logging.disable(logging.CRITICAL)

    app.run()
