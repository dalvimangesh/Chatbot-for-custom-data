import os
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chains import ConversationalRetrievalChain
from langchain.document_loaders.csv_loader import CSVLoader
from langchain.vectorstores import FAISS
from langchain.llms import OpenAI
from langchain.callbacks import get_openai_callback
from dotenv import load_dotenv
import time
import logging

load_dotenv()


class ChatBot:

    def __init__(self, debug=False, model_name = 'text-davinci-003',k = 5, verbose = False) -> None:

        os.environ["OPENAI_API_KEY"] = os.getenv('MY_API_KEY')
        self.__vectorstore = self.__getLoader()
        self.__chain = ConversationalRetrievalChain.from_llm(llm=OpenAI(temperature=0, model_name=model_name),  retriever=self.__vectorstore.as_retriever(search_kwargs={"k": k}), verbose = verbose)
        self.debug = debug

        logger = logging.getLogger('chatBot')  # separate logger for your application to avoid flask logs
        logger.setLevel(logging.INFO)

        file_handler = logging.FileHandler('.log')  # Create a file handler to save logs to a file
        file_handler.setLevel(logging.INFO)

        formatter = logging.Formatter('%(asctime)s - %(message)s')  # Create a formatter to specify the log format
        file_handler.setFormatter(formatter)

        logger.addHandler(file_handler) # Add the file handler to the app logger
        
        self.logger = logger


    def __getLoader(self) -> FAISS:

        embeddings = OpenAIEmbeddings()
        
        dataFiles = os.listdir('data')

        for file in dataFiles: # interating over all data files present

            name = file.split('.')[0]

            if not os.path.exists(f"./vectordb/{name}"): # if index is not created for current file then creating it

                loader = CSVLoader(file_path=f'data/{file}').load()
                vectorstore = FAISS.from_documents(loader, embeddings)    
                vectorstore.save_local(f'vectordb/{name}')
                print(f'index created for {name}')
                # time.sleep(300) # use if getting request limit exceed error

        vectorstore = None

        indexes = os.listdir('vectordb')

        for index in indexes:

            if vectorstore is None:

                vectorstore = FAISS.load_local(f'./vectordb/{index}', embeddings)

            else:

                temp = FAISS.load_local(f'./vectordb/{index}', embeddings)
                vectorstore.merge_from(temp)

        return vectorstore

    '''
    query should be in key-value format as follow
    {
        'question': ...question... ,
        'chat_history': ...list of tuples of previous (human question, ai response)...
    }
    '''
    def response(self, query, id = None) -> str:

        try:

            if self.debug:

                self.logger.info(f'User : {id}')
                
                start = time.time()

                with get_openai_callback() as cb:
                    
                    response = self.__chain(query)
                    self.logger.info( f'Tokens Used: {cb.total_tokens} Prompt Tokens: {cb.prompt_tokens} Completion Tokens: {cb.completion_tokens} Successful Requests: {cb.successful_requests} Total Cost (USD): {cb.total_cost}')

                end = time.time()
                self.logger.info(f'Time Taken : {end - start}')

            else:
                
                response = self.__chain(query)

            self.logger.info(f'Question : { query["question"] } Response : {response["answer"]}')

            return response['answer']

        except:
            
            self.logger.warning('OpenAi not giving response')
            raise Exception('OpenAi not giving response')