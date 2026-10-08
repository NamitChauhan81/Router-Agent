from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from langchain_core.messages import HumanMessage
from pydantic import BaseModel
from typing import List, Dict
from Workflow.Workflow import workflow
import uuid

app = FastAPI(title="Router-Agent_Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    messages: List[Dict[str, str]]
    thread_id: str = "default_thread"

@app.post("/chat")
def ChatEndPoint(request: ChatRequest):
    try:
        thread_ID = request.thread_id
        config = {"configurable": {"thread_id": thread_ID}}

        formatted_message = [HumanMessage(content=msg["content"]) for msg in request.messages]

        # Invoke LangGraph / LangChain workflow
        response = workflow.invoke({"messages": formatted_message}, config=config)
        final_response = response["messages"][-1]
        
        # Safely extract text content whether it's a string or a block list
        content = final_response.content

        if isinstance(content, str):
            final_result = content
        elif isinstance(content, list) and len(content) > 0:
            first_block = content[0]
            if isinstance(first_block, dict) and "text" in first_block:
                final_result = first_block["text"]
            elif hasattr(first_block, "text"):
                final_result = first_block.text
            else:
                final_result = str(first_block)
        else:
            final_result = str(content)

        return {
            "reply": final_result,
            "thread_id": thread_ID
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

 