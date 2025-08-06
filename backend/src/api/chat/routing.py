# routing.py
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from .models import ChatMessagePayload, ChatMessage, ChatMessageListItem
from api.ai.agents import get_supervisor
from api.db import get_session
from api.ai.services import generate_email_message
from api.ai.schemas import EmailMessageSchema, SupervisorMessageSchema
router = APIRouter()

# api/chats/
@router.get("/")
def chat_health():
    return {"status": "ok"}


# /api/chats/recent/
# curl http://localhost:8080/api/chats/recent/
@router.get("/recent/", response_model=List[ChatMessageListItem])
def chat_list_messages(session: Session = Depends(get_session)):
    query = select(ChatMessage) # sql -> query
    results = session.exec(query).fetchall()[:10]
    return results

# HTTP POST -> payload = {"message": "Hello World"} -> {"message":"Hello World", "id":1}
# curl -request method POST -data "JSON data payload" -header "JSON Data" url_endpoint
# curl -X POST -d '{"message": "Hello World"}' -H "Content-Type: application/json" http://localhost:8080/api/chats/
# curl -X POST -d '{"message": "Hello World"}' -H "Content-Type: application/json" https://oyster-app-n4ct3.ondigitalocean.app/api/chats/

# curl -X POST -d '{"message": "Give me a summary as to why it is good to go outside."}' -H "Content-Type: application/json" http://localhost:8080/api/chats/
# curl -X POST -d '{"message": "Research why it is good to go outside and email me the results."}' -H "Content-Type: application/json" http://localhost:8080/api/chats/
@router.post("/", response_model=SupervisorMessageSchema)
def chat_create_message(
    payload:ChatMessagePayload,
    session: Session = Depends(get_session) # need to initialize db session
    ):
    data = payload.model_dump() # pydantic -> dict
    print(data)
    obj = ChatMessage.model_validate(data)
    session.add(obj)
    session.commit()
    supe = get_supervisor()
    msg_data = {
        "messages": [
            {"role":"user",
            "content": f"{payload.message}",
            },
        ]
    }
    result = supe.invoke(msg_data)
    if not result:
        raise HTTPException(status_code=400, detail="error with supervisor")
    messages = result.get("messages")
    if not messages:
         raise HTTPException(status_code=400, detail="error with supervisor")
    return messages[-1]