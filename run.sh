#!/bin/sh

flaskServer() {

    cd server
    . ./server/bin/activate
    export FLASK_APP=app.py
    export FLASK_ENV=development
    flask run

}

reactApp() {

    npm start --prefix ./client

}

flaskServer &
reactApp 