import { useEffect, useRef, useState } from 'react';
import { TypeAnimation } from 'react-type-animation';
import logo from '../assets/logoipsum-331.svg';

function ChatBubbleUser(props){
    return (
        <div className="flex">
            <div className=" max-w-[83.3%] bg-green-400 rounded-md ms-auto">
                <p className="p-4">{props.text}</p>
            </div>
        </div>
    )
}

function ChatBotBubbleProductTable(props){
    let products = props.products ?? []
    return (
        <table className='table-fixed border-spacing-3 divide-y divide-gray-500 border border-gray-500 w-full p-4 mt-4'>
            <tr className='divide-x divide-gray-500'>
                <th className='text-start p-2'>Product</th>
                <th className='text-start p-2'>Shelf Number</th>
            </tr>
            {
                products.map((product, index)=>
                    <tr key={index} className='divide-x divide-gray-500'>
                        <td className='p-2 align-top'>{product[0]}</td>
                        <td className='p-2 align-top'>{product[2]}</td>
                    </tr>)
            }
            
        </table>
    )
}
function ChatBubble(props){
    // replace any \n with br
    const [show_table, setShowTable] = useState(false);
    let text = props.text //.replaceAll("\n", "<br>")
    console.log(props.products);
    return (
        <div className="flex">
            <div className=" max-w-[83.3%] bg-gray-200 rounded-md">
                <p className="p-4" style={{whiteSpace: "pre-line"}}>
                    <TypeAnimation sequence={[text, ()=>{setShowTable(true)}]} speed={65} cursor={false} ca />
                    {
                        (props.products && show_table && props.products.length  > 0) && <ChatBotBubbleProductTable products={props.products} />
                    }
                </p>

            </div>
        </div>
    )
}

function ChatPlaceholder(props){
    let suggesions = [
        "I want to buy coffee.",
        "Do you have fresh milk?."
    ];
    return (
        <div className='w-full h-full flex flex-col items-center justify-center'>
            <img src={logo} alt="logo" className="h-24 mb-6 opacity-55" />
            <div className="flex flex-col">
                <div className='mb-2'>Ask:</div>
                {
                    suggesions.map((suggesion, index)=>(
                        <button className='border py-2 px-4 mb-2 border-gray-400 rounded-md hover:bg-gray-200 text-start'
                            key={index}
                            onClick={()=>{
                                props.sendMessageCallback(suggesion)
                            }}
                        >{suggesion}</button>
                    ))
                }
            </div>
        </div>
    )
}


export default function ChatMessageContainer(props){
    const chatContRef = useRef(null);

    
    let messages_comp = props.messages && props.messages.map((message, index) => {
        if (message.role === "user"){
            return <ChatBubbleUser key={index} text={message.text} />
        } else {
            return <ChatBubble key={index} text={message.text} products={(message.products)?message.products:undefined} />
        }
    })

    useEffect(()=>{
        if (!chatContRef.current) return;
        
        /// Scroll to bottom
        chatContRef.current.scrollTop  = chatContRef.current.scrollHeight;
    }, [props.messages, chatContRef])

    return (
        <div className="flex flex-col h-full overflow-auto p-4 gap-2 pb-20" ref={chatContRef}>
            {messages_comp}
            {props.isReplying && <ChatBubble key={props.messages.length} text=". . ." />}
            {messages_comp.length === 1 && !props.isReplying && <ChatPlaceholder sendMessageCallback={props.sendMessageCallback} />}
        </div>
        
    )
}