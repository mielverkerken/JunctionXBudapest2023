import requests
from fastapi import FastAPI, Request, Response
from pydantic import BaseModel
from starlette.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
import json
from graph import Graph
import configparser
import re
from bs4 import BeautifulSoup


# # Path to your private key file
# private_key_file_path = './private_key.pem'

config = configparser.ConfigParser()
config.read(['config.cfg', 'config.dev.cfg'])
azure_settings = config['azure']
graph: Graph = Graph(azure_settings)
server = "https://fca1-193-225-122-113.ngrok-free.app"

app = FastAPI()

def extractBody(mail):
    soup = BeautifulSoup(mail, "html.parser")
    messageContent = soup.body.text
    return messageContent
    
def sendToServer(message,server):
    messageJson = {"data": [message]}
    response = requests.post(server + "/secrets/scan-email", json=messageJson)
    return response.status_code

@app.get("/")
def read_root():
    return {"Message": "Hello world!"}

# Notification listener endpoint
@app.get('/notification-listen')
async def notification_listen(request: Request):
    return "OK"

@app.post('/notification-listen')
async def notification_listen(request: Request):
    # First, try to retrieve the validation token from query parameters (for subscription validation)  
    # If no validation token, it's an actual notification - process the JSON body
    validation_token = request.query_params.get('validationToken')
    print(validation_token)
    if validation_token:
        #If there's a validation token, respond with it
        print("validation_token=" + validation_token)
        return Response(content=validation_token, media_type="text/plain", status_code=HTTP_200_OK)
    #
    try:
        print("we got a new message in")
        notification_data = await request.json()
        # print(notification_data)
        resource = notification_data['value'][0]['resource'] #e.g. "Users/622eaaff-0683-4862-9de4-f2ec83c2bd98/Messages/AAMkAGUwNjQ4ZjIxAAA="
        # print(resource)
        pattern = r"Users\('([^']+)'\)/messages\('([^']+)'\)"

        # Using regex to find the IDs
        match = re.search(pattern, resource)

        if match:
            user_id = match.group(1)
            message_id = match.group(2)
            print(f"User ID: {user_id}")
            print(f"Message ID: {message_id}")
            mail = await graph.get_mail(user_id,message_id)
            print(mail)
            messageContent = extractBody(str(mail))
            print(messageContent)
            sendToServer(messageContent,server)
        else:
            print("No match found")
        return {'status': 'success'}

    except json.JSONDecodeError:
        # If JSON is invalid or not present
        return Response(status_code=HTTP_400_BAD_REQUEST, content="Invalid JSON")


# Main function to run the script
if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8000)
