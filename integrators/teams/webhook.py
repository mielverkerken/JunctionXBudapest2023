import requests
from fastapi import FastAPI, Request, Response
from pydantic import BaseModel
from starlette.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
import json


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
    validation_token = request.query_params.get('validationToken')
    print("validation_token=" + validation_token)
    if validation_token:
        # If there's a validation token, respond with it
        
        return Response(content=validation_token, media_type="text/plain", status_code=HTTP_200_OK)
    
    # If no validation token, it's an actual notification - process the JSON body
    try:
        notification_data = await request.json()
        print(notification_data)  # Process the notification data
        return {'status': 'success'}
    except json.JSONDecodeError:
        # If JSON is invalid or not present
        return Response(status_code=HTTP_400_BAD_REQUEST, content="Invalid JSON")


# Main function to run the script
if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8000)
