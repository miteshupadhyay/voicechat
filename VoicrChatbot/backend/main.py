#Main Imports
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from decouple import config
import openai

#Custom Function Imports
from functions.openai_requests import convert_audio_to_text, get_chat_response
from functions.database import store_messages,reset_messages
from functions.text_to_speech import convert_text_to_speech

#Initiating App
app = FastAPI()

#CORS - Origins
origins = [
    "http://localhost:5173",
    "http://localhost:5174",
    "http://localhost:4173",
    "http://localhost:4174",
    "http://localhost:3000",
]

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#Check Health
@app.get("/health")
async def check_health():
    print("Mitesh")
    return {"message": "Health"}


# Reset Messages
@app.get("/reset")
async def reset_conversation():
    reset_messages()
    return {"message": "Conversation Reset"}


#Get Audio
@app.post("/post-audio/")
async def post_audio(file: UploadFile = File(...)):

    #Get Saved Audio
    audio_input=open("Voice.mp3","rb")

    #Save file from Front End

    #with open(file.filename,"wb") as buffer:
    #    buffer.write(file.file.read())
    #audio_input = open(file.filename,"rb")

    #Decode Audio
    message_decoded = convert_audio_to_text(audio_input)

    #Guard : Ensure Message Encoded
    if not message_decoded:
        return HTTPException(status_code = 400,detail="Failed to decode the audio")
    
    # Get Chat GPT Response
    chat_response = get_chat_response(message_decoded)

    #Guard : Ensure If No Chat Response
    if not chat_response:
        return HTTPException(status_code = 400,detail="Failed to get the chat response")
    
    # Store messages
    store_messages(message_decoded, chat_response)


    #Convert Chat Response to Audio
    audio_output = convert_text_to_speech(chat_response)

    #Guard : Ensure If No Eleven Lab Response
    if not audio_output:
        return HTTPException(status_code = 400,detail="Failed to get Response from eleven labs")

    # Create a Generator that yields chunks of data
    def iterfile():
        yield audio_output

    # Return Audio File
    return StreamingResponse(iterfile(),media_type="application/octet-stream")

    return "Done"

# Post Bot Response
# Note : Not Playing in Browser when using Post Request
@app.post("/post-audio1/")
async def post_audio(file: UploadFile =File(...)):
    print("hello")