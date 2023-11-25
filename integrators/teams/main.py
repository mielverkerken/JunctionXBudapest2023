import asyncio
import configparser
from msgraph.generated.models.o_data_errors.o_data_error import ODataError
from graph import Graph

async def main():
    print('Python Graph App-Only Tutorial\n')

    # Load settings
    config = configparser.ConfigParser()
    config.read(['config.cfg', 'config.dev.cfg'])
    azure_settings = config['azure']

    graph: Graph = Graph(azure_settings)

    choice = -1

    while choice != 0:
        print('Please choose one of the following options:')
        print('0. Exit')
        print('1. Display access token')
        print('2. List users')
        print('3. Get chat ids from user')
        print('4. Get all chat messages from chat')
        print('5. Get all chat messages from user')
        print('6. create subscription all message changes')
        print('7. create subscription all mail changes from user')

        try:
            choice = int(input())
        except ValueError:
            choice = -1

        try:
            if choice == 0:
                print('Goodbye...')
            elif choice == 1:
                await display_access_token(graph)
            elif choice == 2:
                await list_users(graph)
            elif choice == 3:
                await get_chatids_from_user(graph)
            elif choice == 4:
                await get_chatmessages_from_chat(graph)
            elif choice == 5:
                await get_allchatmessages_from_user(graph)
            elif choice == 6:
                await create_subscription_all_message_changes(graph)
            elif choice == 7:
                await create_subscription_all_mail_changes_from_user(graph)
            else:
                print('Invalid choice!\n')
        except ODataError as odata_error:
            print('Error:')
            if odata_error.error:
                print(odata_error.error.code, odata_error.error.message)


async def display_access_token(graph: Graph):
    token = await graph.get_app_only_token()
    print('App-only token:', token, '\n')

async def list_users(graph: Graph):
    users_page = await graph.get_users()

    # Output each users's details
    if users_page and users_page.value:
        for user in users_page.value:
            print('User:', user.display_name)
            print('  ID:', user.id)
            print('  Email:', user.mail)

        # If @odata.nextLink is present
        more_available = users_page.odata_next_link is not None
        print('\nMore users available?', more_available, '\n')

async def get_chatids_from_user(graph: Graph):
    id="099ba34e-ce8b-4660-84de-7911e9c3a4ef"
    chats = await graph.get_chatids_from_user(id)
    print(chats)

async def get_chatmessages_from_chat(graph: Graph):
    id="099ba34e-ce8b-4660-84de-7911e9c3a4ef"
    chatid = "19:082bc55a-3db4-4906-99c5-a66fb20297e3_099ba34e-ce8b-4660-84de-7911e9c3a4ef@unq.gbl.spaces"
    chats = await graph.get_chatmessages_from_chat(id, chatid)
    print(chats)

async def get_allchatmessages_from_user(graph: Graph):
    id="099ba34e-ce8b-4660-84de-7911e9c3a4ef"
    chats = await graph.get_allchatmessages_from_user(id)
    print(chats)

async def create_subscription_all_message_changes(graph: Graph):
    result = await graph.create_subscription_all_message_changes()
    print(result)

async def create_subscription_all_mail_changes_from_user(graph: Graph):
    id="099ba34e-ce8b-4660-84de-7911e9c3a4ef"
    result = await graph.create_subscription_all_mail_changes_from_user(id)
    print(result)



# Run main
asyncio.run(main())
