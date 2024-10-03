import './message.css'
import robot from '../../../images/robot.svg'
import user from '../../../images/user.svg'

function Message({ text, who, infoHandler , typingStatus }) {

    let color = null
    let whichCorner = null

    if(infoHandler !== undefined){ // to indentify msg is containing info or not
        whichCorner = '-info'
        color = 'info'
    }
    else  if (who === 'Ai') { // normal Ai msg
        whichCorner = '-Normal'
        color = 'primary'
    }
    else { // normal Humnan msg
        whichCorner = ''
        color = 'secondary'
    }

    return (
        <div className={who + "-msg"}   >

            <img src={ who === 'Ai' ? robot : user } className="rounded-circle m-2 img-fluid" alt="" />

            {
                typingStatus ? <div className={`${who}-text p-3`} >  <div className="dot-typing m-1"></div> </div>
                    : <div className={`${who}-text p-3 m-2 bg-${color} bg-opacity-10  border-${color} rounded-4 chat-bubble chat-bubble--${who + whichCorner}`} > {text} </div>
            }

        </div>

    )

}

export default Message
