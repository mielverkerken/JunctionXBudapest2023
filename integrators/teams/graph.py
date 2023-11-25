from configparser import SectionProxy
from azure.identity.aio import ClientSecretCredential
from msgraph import GraphServiceClient
from msgraph.generated.users.users_request_builder import UsersRequestBuilder
import requests
from datetime import datetime, timedelta

class Graph:
    settings: SectionProxy
    client_credential: ClientSecretCredential
    app_client: GraphServiceClient

    def __init__(self, config: SectionProxy):
        self.settings = config
        client_id = self.settings['clientId']
        tenant_id = self.settings['tenantId']
        print(tenant_id)
        client_secret = self.settings['clientSecret']
        
        self.notification_url = self.settings['notificationUrl']
        self.client_credential = ClientSecretCredential(tenant_id, client_id, client_secret)
        self.app_client = GraphServiceClient(self.client_credential) # type: ignore


    async def get_app_only_token(self):
        graph_scope = 'https://graph.microsoft.com/.default'
        access_token = await self.client_credential.get_token(graph_scope)
        return access_token.token

    async def get_users(self):
        query_params = UsersRequestBuilder.UsersRequestBuilderGetQueryParameters(
                # Only request specific properties
                select = ['displayName', 'id', 'mail'],
                # Get at most 25 results
                top = 25,
                # Sort by display name
                orderby= ['displayName']
            )
        request_config = UsersRequestBuilder.UsersRequestBuilderGetRequestConfiguration(
                query_parameters=query_params
            )

        users = await self.app_client.users.get(request_configuration=request_config)
        return users

    async def get_chatids_from_user(self, id):
        result = await self.app_client.users.by_user_id(id).chats.get()
        return result

    async def get_chatmessages_from_chat(self, id, chatid):
        result = await self.app_client.users.by_user_id(id).chats.by_chat_id(chatid).messages.get()
        return result

    # https://learn.microsoft.com/en-us/graph/api/chats-getallmessages?view=graph-rest-1.0&tabs=python#request
    async def get_allchatmessages_from_user(self, id):
        result = await self.app_client.users.by_user_id(id).chats.get_all_messages.get()
        return result
    
    async def create_subscription_all_message_changes(self):
        # URL and headers for the POST request
        url = "https://graph.microsoft.com/v1.0/subscriptions"
        token = await self.get_app_only_token()
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + token
        }

        # specify time 5 mins from now
        expiration_datetime = (datetime.utcnow() + timedelta(minutes=5)).isoformat() + "Z"

        data = {
            # "changeType": "updated",
            "changeType": "created,updated",
            "notificationUrl": self.notification_url,
            # "resource": "/chats/19:082bc55a-3db4-4906-99c5-a66fb20297e3_099ba34e-ce8b-4660-84de-7911e9c3a4ef@unq.gbl.spaces",
            "resource": "/chats",
            "includeResourceData": False,
            # "includeResourceData": True,
            # "encryptionCertificate": "MIIFATCCAukCFCnNf1HIm6AntGM7/DE2w5L458bxMA0GCSqGSIb3DQEBCwUAMD0xCzAJBgNVBAYTAkJFMQwwCgYDVQQIDANXVkwxDjAMBgNVBAcMBUdoZW50MRAwDgYDVQQKDAdBbGxTZWVrMB4XDTIzMTEyNTA3MDMwN1oXDTI0MTEyNDA3MDMwN1owPTELMAkGA1UEBhMCQkUxDDAKBgNVBAgMA1dWTDEOMAwGA1UEBwwFR2hlbnQxEDAOBgNVBAoMB0FsbFNlZWswggIiMA0GCSqGSIb3DQEBAQUAA4ICDwAwggIKAoICAQC6BN83o/xc/Dga+sXz3y53yBHR9TrmkjYfGvORr90GovLAUfqp1E+KG7x6YwHqjHlCSwrCXsiNkv/vQQKBvSc6zW7riPq5NOdVGkYtsjSlKD8gjZ+yAWOa7X+mnHdvtMC/X6yvi7qI40ohAE88ObMLjZVOINCgLNm62GJYbZ/ceorG9mZN8W2smym0rZXzKzXLIAj90g9CxIiMYKshdJCz5pPBeb0wRYVoArfoxbHqdbFlw77xVxYUJWHtlKtObsDVho6Z0HeYy3Nt7aAtFW9QPbmM3ikQn6idOe22xyC6WjgFparRu15fskHhiJi/+O2UFLdHPOLHSzcPaxcrxnJnjXO3GT/ppZaG3KsJcaWWualLW5LdyFZ4BBNzfzzVAgNfJ/bQVJ3yU44GSPBOTHL0+qm4Zsm6zMXi0Vs1mfImY9176J7uYPkJwgPMdp1QGsMNy5HbpRHYmmIFWxJJqWmF4fH7lHubEK6XKdxMF2VZnwq8/lOD2DVflj3TfELw6hfBuBQXrI19Qxx4D7rHZi1RzOIH7Z0xhZZ0adTQ59fwzlX1D+B1adjnbzxOZJ2iCecn7LsNcGtXjVNS3lmrhRidQZi5/lOGQhRVCpnrtn3slUCAbO2aQmQgMEj0EVGzVKBE+ZiurmAikt0mGVyRtHmxy5eXDg+slI2kpMax0qqZ/wIDAQABMA0GCSqGSIb3DQEBCwUAA4ICAQC0ngMf6o+653xaTrTgN7f2+d7GOfy/J0I9SX1+iBv1/q4pYI/UFWzbrhH0kpJONDoo2lKBr7KutaYS8ZjSbw+GqYxQuz+D7jq/02JXzmJbCefo1gdAQEx3h75SuIehKVSGQqR7G0IJ40PkhkoEuo/9BmRvMnbXQJjTKKerYL1eN3XpxUBPl0uE9RePU4ZHtIqHuU0mQ3l1PpH9d4NVALucJOObnlAx9zvvAzYP0wBUEAtd0FPW8+Obm8okmvSEE4EFpdQzBcUoQtfqWEpJErP0iNJGrQILh5B0LQ1TL/i3F1qq9rQCocDl1GdyVm4ofL8HxUNYl+9w0FxVyac/e1kUgc/NwViag+DTY++WKZ4CawRI89Vd4PVr/BbQS/z3OKga6eoBw0aHTHgqKAo9wyeeJ5IE/wth22OuRhJofv0/4xIz0YDHoxQew6N1Gv8TQ5QS6YNtOok/4VFe1pDayifumvkvSg3QKTlJERxuJU3/Yw1VUHmDF1qLzaU7OAxbNNC69jCbGTCIpzkh18wZChO7nOmpGKj9773WSwE/PrrRvYjb+1E2WTC5t/7gcFHBYwt7AsBiIfBaC0qZtSk9GHIO1jTqb09z1kEhvE0MVsCaHAhGh9AMu5NigvJUFfX+/ARWB8tByFKb/vPgrtbGK2M7w0MFU3BnnIREPKRYRTVxRA==",  # Replace with your actual certificate
            # "encryptionCertificateId": "junctionKey",               # Replace with your actual custom ID
            "expirationDateTime": expiration_datetime,
            "clientState": "secretclientState"                    # Replace with your actual client state
        }

        response = requests.post(url, json=data, headers=headers)
        print (response.text)
        return response

    async def create_subscription_all_mail_changes_from_user(self, id):
        # URL and headers for the POST request
        url = "https://graph.microsoft.com/v1.0/subscriptions"
        token = await self.get_app_only_token()
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + token
        }

        # specify time 5 mins from now
        expiration_datetime = (datetime.utcnow() + timedelta(minutes=5)).isoformat() + "Z"

        data = {
            "changeType": "created",
            "notificationUrl": self.notification_url,
            "resource": f"/users/{id}/messages?$select=Subject,bodyPreview,importance,receivedDateTime,from",
            #"includeResourceData": False,
            "includeResourceData": True,
            "encryptionCertificate": "MIIFATCCAukCFCnNf1HIm6AntGM7/DE2w5L458bxMA0GCSqGSIb3DQEBCwUAMD0xCzAJBgNVBAYTAkJFMQwwCgYDVQQIDANXVkwxDjAMBgNVBAcMBUdoZW50MRAwDgYDVQQKDAdBbGxTZWVrMB4XDTIzMTEyNTA3MDMwN1oXDTI0MTEyNDA3MDMwN1owPTELMAkGA1UEBhMCQkUxDDAKBgNVBAgMA1dWTDEOMAwGA1UEBwwFR2hlbnQxEDAOBgNVBAoMB0FsbFNlZWswggIiMA0GCSqGSIb3DQEBAQUAA4ICDwAwggIKAoICAQC6BN83o/xc/Dga+sXz3y53yBHR9TrmkjYfGvORr90GovLAUfqp1E+KG7x6YwHqjHlCSwrCXsiNkv/vQQKBvSc6zW7riPq5NOdVGkYtsjSlKD8gjZ+yAWOa7X+mnHdvtMC/X6yvi7qI40ohAE88ObMLjZVOINCgLNm62GJYbZ/ceorG9mZN8W2smym0rZXzKzXLIAj90g9CxIiMYKshdJCz5pPBeb0wRYVoArfoxbHqdbFlw77xVxYUJWHtlKtObsDVho6Z0HeYy3Nt7aAtFW9QPbmM3ikQn6idOe22xyC6WjgFparRu15fskHhiJi/+O2UFLdHPOLHSzcPaxcrxnJnjXO3GT/ppZaG3KsJcaWWualLW5LdyFZ4BBNzfzzVAgNfJ/bQVJ3yU44GSPBOTHL0+qm4Zsm6zMXi0Vs1mfImY9176J7uYPkJwgPMdp1QGsMNy5HbpRHYmmIFWxJJqWmF4fH7lHubEK6XKdxMF2VZnwq8/lOD2DVflj3TfELw6hfBuBQXrI19Qxx4D7rHZi1RzOIH7Z0xhZZ0adTQ59fwzlX1D+B1adjnbzxOZJ2iCecn7LsNcGtXjVNS3lmrhRidQZi5/lOGQhRVCpnrtn3slUCAbO2aQmQgMEj0EVGzVKBE+ZiurmAikt0mGVyRtHmxy5eXDg+slI2kpMax0qqZ/wIDAQABMA0GCSqGSIb3DQEBCwUAA4ICAQC0ngMf6o+653xaTrTgN7f2+d7GOfy/J0I9SX1+iBv1/q4pYI/UFWzbrhH0kpJONDoo2lKBr7KutaYS8ZjSbw+GqYxQuz+D7jq/02JXzmJbCefo1gdAQEx3h75SuIehKVSGQqR7G0IJ40PkhkoEuo/9BmRvMnbXQJjTKKerYL1eN3XpxUBPl0uE9RePU4ZHtIqHuU0mQ3l1PpH9d4NVALucJOObnlAx9zvvAzYP0wBUEAtd0FPW8+Obm8okmvSEE4EFpdQzBcUoQtfqWEpJErP0iNJGrQILh5B0LQ1TL/i3F1qq9rQCocDl1GdyVm4ofL8HxUNYl+9w0FxVyac/e1kUgc/NwViag+DTY++WKZ4CawRI89Vd4PVr/BbQS/z3OKga6eoBw0aHTHgqKAo9wyeeJ5IE/wth22OuRhJofv0/4xIz0YDHoxQew6N1Gv8TQ5QS6YNtOok/4VFe1pDayifumvkvSg3QKTlJERxuJU3/Yw1VUHmDF1qLzaU7OAxbNNC69jCbGTCIpzkh18wZChO7nOmpGKj9773WSwE/PrrRvYjb+1E2WTC5t/7gcFHBYwt7AsBiIfBaC0qZtSk9GHIO1jTqb09z1kEhvE0MVsCaHAhGh9AMu5NigvJUFfX+/ARWB8tByFKb/vPgrtbGK2M7w0MFU3BnnIREPKRYRTVxRA==",  # Replace with your actual certificate
            "encryptionCertificateId": "junctionKey",               # Replace with your actual custom ID
            "expirationDateTime": expiration_datetime,
            "clientState": "secretclientState"                    # Replace with your actual client state
        }

        response = requests.post(url, json=data, headers=headers)
        print (response.text)
        return response


    async def get_mail(self, id, messageid):
        print(id)
        print (messageid)
        result = await self.app_client.users.by_user_id(id).messages.by_message_id(messageid).get()
        return result