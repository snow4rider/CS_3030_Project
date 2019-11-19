import requests, json

class ClientUser:
    username, password = ""

    def login(self):
        apiCall = "http://127.0.0.1:8000/api-auth/login/"

        self.username = input("Enter your username: ")
        self.password = input("Enter your password: ")

        # Authenticate


    def checkMessages():
        apiCall = "http://127.0.0.1:8000/users/"

        jsonStr = requests.get(apiCall).text
        allUsers = json.loads(jsonStr)
        #user = allUsers


    def sendMessage(recipient, message):
        apiCall = "http://127.0.0.1:8000/messages/"

        message = {
            'text': message,
            'recipient': recipient
        }

        response = requests.post(apiCall, data=message, auth=("gatkins2", "bloog890"))


# start of client
user = ClientUser()
user.login()

# display menu
while True:
    print("1. Check messages")
    print("2. Send a message")
    print("(0 to exit)")

    selection = input("What would you like to do?:")
    if selection == 1:
        user.checkMessages()
    elif selection == 2:
        user.sendMessage()
    elif selection == 0:
        break
    else:
        continue
