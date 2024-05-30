import json
import random

#Get Recent Messages

def get_recent_messages():

    #Define the file name and learn instruction
    file_name="stored_data.json"
    learn_instruction = {
        "role":"system",
        "content":"you are interviewing the user for a job as a retail assistant. Ask short questions that are relevant to the junior position. Your Name is Riya. The user is called Mitesh. Keep your answers to under 30 words"
    }

    #Initialize Messages
    messages = []

    #Add a random element
    x= random.uniform(0,1)
    if x<0.5:
        learn_instruction["content"] = learn_instruction["content"]+ " your response will include some dry humor."
    else:
        learn_instruction["content"] = learn_instruction["content"]+ " your response will include rather a challanging question."        

 #Append Instructions to the messages
    messages.append(learn_instruction)

    #Get Last Messages
    try:
        with open(file_name) as user_file:
            data = json.load(user_file)

        # Append last 5 items of data
            if data:
                if len(data) < 5:
                    for item in data:
                        messages.append(item)
                else:
                    for item in data[-5:]:
                        messages.append(item)
    except Exception as e:
        print(e)
        pass

    #Return Messages
    return messages

# Store Messages
def store_messages(request_message,response_message):
    
    # Define the file name
    file_name = "stored_data.json"

    # Get Recent Messages
    messages = get_recent_messages()[1:]

    # Add Messages to Data
    user_message = {"role": "user","content":request_message}
    assistant_message = {"role": "assistant","content":response_message}
    messages.append(user_message)
    messages.append(assistant_message)


    #Save the updated File
    with open(file_name,"w") as f:
        json.dump(messages,f)

    # Reset Messages
def reset_messages():

 #overwrite Current file with nothing
 open("stored_data.json","w")


 
