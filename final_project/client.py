import json
import requests


class ClientUser:
    # API Calls
    baseCall = "http://127.0.0.1:8000/"
    allUsers = "users/"
    allMessages = "messages/"

    # User info
    username = ""
    password = ""
    id = 0
    friends = {}


    def login(self):
        self.username = input("Enter your username: ")
        self.password = input("Enter your password: ")

        # Authenticate
        res = requests.get(self.baseCall + self.allUsers).text
        usersList = json.loads(res)
        for user in usersList:
            if user['username'] == self.username:
                self.id = user['id']
                break
        if self.id == 0:
            print("User not found")
            self.username = ""
            self.password = ""
            return False
        res = requests.get(self.baseCall + "user/" + str(self.id) + "/", auth=(self.username, self.password))
        if res.status_code != 200:
            print("Invalid username or password")
            self.username = ""
            self.password = ""
            self.id = 0
            return False

        # Return true if authenticated
        return True


    def addFriend(self):
        friendUsername = input("Username of new friend: ")

        if friendUsername in self.friends.keys():
            print("Friend already added\n")
            return

        # Search for friend in database
        res = requests.get(self.baseCall + self.allUsers).text
        allUsers = json.loads(res)
        for user in allUsers:
            if user['username'] == friendUsername:
                self.friends[friendUsername] = user['id']
                print("Friend added\n")
                return

        # If user is not found
        print("User not found\n")


    def retrieveMessages(self):

        newMessages = []

        # Check for messages where user is the recipient
        res = requests.get(self.baseCall + self.allMessages).text
        messages = json.loads(res)
        for message in messages:
            if message['recipient'] == self.username:
                newMessages.append(message)
        return newMessages


    def checkMessages(self, messages):
        for message in messages:
            print("Message from " + message['sender'] + ":")
            print("\t" + message['text'] + "\n")



    def sendMessage(self):

        # Get recipient
        recipient = input("Which friend would you like to message?: ")
        if recipient not in self.friends.keys():
            print("Friend not found\n")
            return

        # Send message
        message = input("Enter your message: ")
        message = {
            'text': message,
            'recipient': recipient
        }

        res = requests.post(self.baseCall + self.allMessages, data=message, auth=(self.username, self.password))
        if res.status_code != 201:
            print("An error occured: Message not sent\n")
        else:
            print("Meesage sent\n")


# start of client
user = ClientUser()
loggedIn = False
while not loggedIn:
    loggedIn = user.login()
    print()

# display menu
while True:
    print("1. Add a friend")
    print("2. Check messages")
    print("3. Send a message")
    print("(0 to exit)")

    selection = int(input("What would you like to do?:"))
    if selection == 1:
        user.addFriend()
    elif selection == 2:
        newMessages = user.retrieveMessages()
        print(f"\nYou have {len(newMessages)} new messages\n")
        view = input("View now? (Y/N): ").lower()
        if view == 'y':
            user.checkMessages(newMessages)
    elif selection == 3:
        user.sendMessage()
    elif selection == 0:
        break
    else:
        continue
