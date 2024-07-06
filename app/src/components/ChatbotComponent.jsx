import ChatMessageContainer from "./ChatContainer";
import ChatInput from "./ChatInput";
import logo from '../assets/logoipsum-331.svg';
import { useCallback, useState } from "react";


const sampleMessages = [
    {
        role: "assistant",
        text: "Hello, how can I help you?"
    },
]

async function getReply(message){
    const url = '/api/ask';
    const response = await fetch(url, {
        method: 'POST',
        body: JSON.stringify({question:message}),
        headers: {
            'Content-Type': 'application/json'
        }
    });
    if (response.ok){
        const data = await response.json();
        return {
            text: data.response,
            products: data.products
        }
    }
}

export default function ChatbotBody(){
    const [messages, setMessages] = useState(sampleMessages);
    const [isReplying, setIsReplying] = useState(false);

    const sendMessageCallback = useCallback((message)=>{
        const user_message = {role: "user", text: message}
        setMessages([...messages, user_message])
        setIsReplying(true);

        getReply(message).then((reply)=>{
            let msg =  {role: "assistant", text: reply.text}
            if (reply.products && reply.products.length > 0){
                msg.products = reply.products
            }
            setMessages([...messages, user_message, msg])
            setIsReplying(false);
        }).catch((e)=>{
            console.error(e);
            setMessages([...messages, {role: "assistant", text: "I'm sorry, I cannot help you with that."}])
            setIsReplying(false);
        });
    }, [messages])

    return (
        <div className="border lg:max-w-[680px] w-full h-full flex flex-col mx-auto relative overflow-clip flex-grow">
            <header className="py-3 px-4 shadow-md z-10 flex gap-4 justify-center items-center">
                <div className="flex items-center justify-center">
                    <img src={logo} alt="logo" className="h-12" />
                    <h1 className='text-center text-2xl font-bold my-3'>Sunny Super</h1>
                </div>
            </header>
            <ChatMessageContainer messages={messages} isReplying={isReplying} sendMessageCallback={sendMessageCallback} />
            <ChatInput sendMessageCallback={sendMessageCallback} isReplying={isReplying} />
        </div>
    )
}