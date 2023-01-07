import sys
sys.dont_write_bytecode = True
from fastapi import FastAPI
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from pydantic import EmailStr, BaseModel
from typing import List
from dotenv import load_dotenv
import os
from redis import Redis

load_dotenv()

SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")
USERNAME = os.getenv("USERNAME")
SENDING_EMAIL = os.getenv("SENDING_EMAIL")
PORT = os.getenv("PORT")
HOST = os.getenv("HOST")


conf = ConnectionConfig(
    MAIL_USERNAME = USERNAME,
    MAIL_PASSWORD = SENDGRID_API_KEY,
    MAIL_FROM = SENDING_EMAIL,
    MAIL_PORT = PORT,
    MAIL_SERVER = HOST,
    MAIL_FROM_NAME="Ieloro Marketplace",
    MAIL_STARTTLS = True,
    MAIL_SSL_TLS = False,
    USE_CREDENTIALS = True,
    VALIDATE_CERTS = False
)

app = FastAPI()

@app.on_event("startup")
def startup_db_client():
    app.redis_client = Redis(host="docker.for.mac.localhost", port=6379, decode_responses=True)


@app.on_event("shutdown")
def shutdown_db_client():
    app.mongodb_client.close()

app.include_router(user_router)

@app.post("/verify-email")
async def simple_send(email: str):
    html = """<p>Hi this test mail, thanks for using Fastapi-mail</p> """

    message = MessageSchema(
        subject="Fastapi-Mail module",
        recipients=email,
        body=html,
        subtype=MessageType.html)

    fm = FastMail(conf)
    await fm.send_message(message)
    return {"message": "email has been sent"}
