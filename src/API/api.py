from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from langchain_core.messages import HumanMessage
from pydantic import BaseModel, Field
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
    messages :List[Dict[str, str]]
    thread_id : str = "default_thread"


@app.post("/chat")
def ChatEndPoint(request:ChatRequest):
    try:
         
         thread_ID = request.thread_id
  
         config = {"configurable":{"thread_id": thread_ID}}

         formatted_message = [HumanMessage(content = msg["content"])  for msg in request.messages]


         response =  workflow.invoke({"messages":formatted_message}, config=config)
         final_response = response["messages"][-1]
         result = final_response.content
         final_result = result[0]["text"]



         return{"reply":final_result,
           "thread_id":thread_ID}
    except Exception as e :
        raise HTTPException(status_code=500, detail= str(e))


 