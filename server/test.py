from chatbot import ChatBot
import time
chatbot = ChatBot(debug=True, k = 10, verbose = False)

memory = []


while True:

    query = input('Q --> ')

    if(query=='bye'):
        break
    
    s = time.time()

    finalQuery = { 'question' : query , 'chat_history' : memory }

    print(finalQuery)

    response = chatbot.response(finalQuery)

    memory.append((query,response))

    e = time.time()

    print(e-s)