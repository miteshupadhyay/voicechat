import requests
from decouple import config

ELEVEN_LABS_API_KEY=config("ELEVEN_LABS_API_KEY")

# ELEVEN LABS
# Convert Text to Speech

def convert_text_to_speech(message):

#Define Data (Body)
    
  body = {
   "text" : message,
   "voice_settings":{
     "stability": 0,
     "similarity_boost":0,
    }
  }
    
    # Define Voice
  voice_rachel= "21m00Tcm4TlvDq8ikWAM"

#Constructing Headers and Endpoints
  headers = {"ai-api-key": ELEVEN_LABS_API_KEY, "Content-Type": "application/json","accept":"audio/mpeg"}
  endpoint= f"https://api.elevenlabs.io/v1/text-to-speech/{voice_rachel}"

#Send Requests
  try:
    response=requests.post(endpoint,json=body,headers=headers)
  except Exception as e:
   return


#Handle Response
  if response.status_code == 200:
    return response.content
  else:
    return