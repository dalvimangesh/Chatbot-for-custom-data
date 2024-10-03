# Running Flask Server and React App

## Folder Structure

- root directory
  - server
    - app.py
    - chatbot.py
    - data
    - requirements.txt
    - readme.md ( steps to set up flask environment )
    - (other flask server files)
    
  - client

    - package.json
    - readme.md ( steps to set up react environment )
    - (other React app files)
  - run.sh

## Running the Script
1. Please make sure you have completed all the necessary setup requirements for both the Flask server and React app by carefully following the instructions provided in the markdown files located in their respective directories. 

2. Give executable permissions to run.sh 

        chmod +x run.sh

3. Run server and client

        ./run.sh

4. To stop the Flask server and React server

    Run the following command to view the list of running processes
 
        ps -a
       
    Identify the process IDs associated with the Flask server and React server processes in the displayed list.
    
    To stop the server, execute the following command, replacing <server_pid> with the actual process ID of the server
    
        kill <server_pid>
