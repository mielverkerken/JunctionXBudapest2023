# Teams Integrator

## Set up webhook server  

Set up an ngrok tunnel to listen to change notifications

    brew install ngrok 
    ngrok config add-authtoken {token}
    ngrok http 8000

run the webhook server

    python3 webhook.py

## Configure subscription script

Configure the config.cfg file in the directory (values can be found in notion)

Run the graph api test script

    python3 main.py

for subscription, select option 6 or 7

send a message in teams and there should be a notification on your webhook but this doesn't work yet


## references

https://learn.microsoft.com/en-us/graph/teams-changenotifications-chatmessage#subscribe-to-messages-of-any-chat-in-a-tenant-where-a-specific-teams-app-is-installed 
