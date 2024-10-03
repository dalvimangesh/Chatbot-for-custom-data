import { useState, useEffect, useRef } from 'react';
import './App.css';
import Chat from './components/chat/Chat';
import InputBar from './components/inputbar/Inputbar'
import axios from 'axios'
import '../node_modules/bootstrap/dist/css/bootstrap.min.css'
import './scss/main.css'

function App() {

  const [chats, setChats] = useState([])
  const [userMsg, setUserMsg] = useState('')
  const [userId, setUserId] = useState('')
  const [typingStatus, setTypingStatus] = useState(false)
  const [apiStatus, setApiStatus] = useState(true)
  const buttonRef = useRef(null)
  const inputRef = useRef(null)

  // Fetching the unique key from the flask-server
  // only once for each user session
  // In strict mode , this will get executed twice
  useEffect(() => {

    const callFlaskServer = async () => {

      try {

        const res = await axios.get('http://127.0.0.1:5000/generate', { headers: { 'X-API-KEY': process.env.REACT_APP_X_API_KEY } })
        setUserId(() => res.data['userId'])
        const body = { "id": res.data['userId'], "question": '' }
        const starter = await axios.post('http://127.0.0.1:5000/chat', body, { headers: { 'X-API-KEY': process.env.REACT_APP_X_API_KEY } })
        setChats([{ 'who': 'Ai', 'msg': starter.data['answer'] }])

      }
      catch (e) {
        setApiStatus(false)
      }
    }

    callFlaskServer()

  }, [apiStatus])

  // onSubmit handler for form
  // if user is submitting same msg again then restricting it from doing it
  // disabling the input text and input buttons
  async function getResponse(event) {

    event.preventDefault();
    let inputMsgEntered = event.target['inputMsg'].value

    if (inputMsgEntered === userMsg) {
      return
    }

    buttonRef.current.className = 'btn btn-primary disabled h-100 me-2'
    inputRef.current.setAttribute('disabled', true);
    setUserMsg((_) => inputMsgEntered)
    setChats(allChats => [...allChats, { 'who': 'User', 'msg': inputMsgEntered }])
    setChats(allChats => [...allChats, { 'who': 'Ai', 'msg': '' }])
    setTypingStatus(true)

    try {

      const body = { "id": userId, "question": inputMsgEntered }
      const res = await axios.post('http://127.0.0.1:5000/chat', body, { headers: { 'X-API-KEY': process.env.REACT_APP_X_API_KEY } })
      setChats((allChats) => {
        allChats[allChats.length - 1].msg = res.data['answer']
        return allChats
      })

      buttonRef.current.className = 'btn btn-outline-success h-100 me-2'
      inputRef.current.removeAttribute('disabled')
      setTypingStatus(false)

    }
    catch (e) { // Handling two errors internal server error or session expired

      // if session has expired then disabling the inputs
      // if there is internal server error then not disabling the inputs

      let msgToShow = ''
      if (e.response !== undefined && e.response.status !== undefined && e.response.status === 403) {
        msgToShow = `Uh-oh! ⌛️🔒 It seems your session has expired. No worries, let's get you back in action! Please consider reloading page again to continue. 🚀🔑`
      }
      else {
        msgToShow = `Whoops! 🤖😵 Looks like we're experiencing some technical difficulties at the moment. Please bear with us while we fix the issue. 💪🔧`
      }
      setTypingStatus(false)
      setChats((allChats) => {
        allChats[allChats.length - 1].msg = msgToShow
        allChats[allChats.length - 1].info = true // new property to indentify msg is containing info
        return allChats
      })

      if (e.response === undefined || e.response.status === undefined || e.response.status !== 403) {
        buttonRef.current.className = 'btn btn-outline-success h-100 me-2'
        inputRef.current.removeAttribute('disabled')
      }

    }

  }

  // Main app consists of two major components
  // one for showing all chat logs
  // other for taking input and submit button
  return (
    <div className="App container-md vh-100 bg-light shadow bg-body rounded p-0">

      <Chat chats={chats} typingStatus={typingStatus} />
      <InputBar onSubmitHandler={getResponse} buttonHandler={buttonRef} inputHandler={inputRef} apiHandler={apiStatus} />

    </div>
  );
}

export default App;
