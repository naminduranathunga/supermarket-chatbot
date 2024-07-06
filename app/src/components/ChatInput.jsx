import { Send } from 'lucide-react';
import { useState } from 'react';

export default function ChatInput(props){
    const [message, setMessage] = useState("");
    const sendFn = ()=>{
        if (props.isReplying === true) return;

        let message_ = message.trim();
        if (message_ && typeof props.sendMessageCallback === "function"){
            props.sendMessageCallback(message_);
        }
        setMessage("");
    }
    const onkeydown = (e)=>{
        if (e.key === "Enter" && e.shiftKey === false){
            sendFn();
        }
    }

    return (
        <div className="flex absolute bottom-0 left-0 bg-white w-full pb-4 border-t-4">
            <input type="text" value={message}
                onChange={(e)=>setMessage(e.target.value)}
                onKeyDown={onkeydown}
                className="w-full py-3.5 px-8 outline-none" placeholder="Message..."  />
            <button className="bg-white text-black hover:text-gray-600 hover:bg-gray-200 px-4 duration-200 transition" onClick={sendFn} disabled={props.isReplying === true}>
                <Send />
            </button>
        </div>
    )
}