import { useRef, useEffect } from 'react';
import Message from './message/Message';

function Chat({ chats , typingStatus }) {

    const messagesEndRef = useRef(null)

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: "smooth" })
    }

    useEffect(() => {
        scrollToBottom()
    }, [chats,typingStatus]); // as typing status changed we will render that msg again

    return (
        
        <div className='container-lg overflow-auto chat-history p-4' >

            {
                chats.map((msg , index) => {

                    // Ai msg can never be '' from flask-server so this will not give any conflict to detect msg for which we are waiting

                    return <Message text={msg.msg} who={msg.who} key={index} infoHandler = {msg.info} typingStatus = { msg.who === 'Ai' && msg.msg === '' ? typingStatus : false } />

                })
            }

            <div ref={messagesEndRef} />

        </div>
    )
}

export default Chat;
