import requests
from fastapi import FastAPI, Request, Response
from pydantic import BaseModel
from starlette.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
import json

# Path to your private key file
private_key_file_path = './private_key.pem'

app = FastAPI()

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
    if validation_token:
        #If there's a validation token, respond with it
        print("validation_token=" + validation_token)
        return Response(content=validation_token, media_type="text/plain", status_code=HTTP_200_OK)
    #
    try:
        notification_data = await request.json()
        print(notification_data)
        resource = notification_data['value'][0]['resource'] #e.g. "Users/622eaaff-0683-4862-9de4-f2ec83c2bd98/Messages/AAMkAGUwNjQ4ZjIxAAA="
        return {'status': 'success'}

    except json.JSONDecodeError:
        # If JSON is invalid or not present
        return Response(status_code=HTTP_400_BAD_REQUEST, content="Invalid JSON")


# Main function to run the script
if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8000)
