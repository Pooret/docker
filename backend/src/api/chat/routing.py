# routing.py
from typing import List
from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from .models import ChatMessagePayload, ChatMessage, ChatMessageListItem
from api.db import get_session
from api.ai.services import generate_email_message
from api.ai.schemas import EmailMessageSchema
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

@router.post("/", response_model=EmailMessageSchema)
def chat_create_message(
    payload:ChatMessagePayload,
    session: Session = Depends(get_session) # need to initialize db session
    ):
    data = payload.model_dump() # pydantic -> dict
    print(data)
    obj = ChatMessage.model_validate(data)
    session.add(obj)
    session.commit()
    #session.refresh(obj) # ensure id/primary key is added to object instance
    # ready to store in the database
    response = generate_email_message(payload.message)
    return response