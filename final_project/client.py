import json
import requests
import webbrowser


class ClientUser:
    # API Calls
    baseCall = "http://127.0.0.1:8000/"
    allProfiles = "profiles/"
    allMessages = "messages/"

    # User info
    username = ""
    password = ""
    id = 0
    friends = {}

    def register(self):
        webbrowser.open_new(self.baseCall + 'register/')


    def login(self):
        self.username = input("Enter your username: ")
        self.password = input("Enter your password: ")

        # Authenticate
        res = requests.get(self.baseCall + self.allProfiles)
        usersList = json.loads(res.text)
        for user in usersList:
            if user['username'] == self.username:
                self.id = user['id']
                break
        if self.id == 0:
            print("User not found")
            self.username = ""
            self.password = ""
            return False
        res = requests.get(self.baseCall + "profile/" + str(self.id) + "/", auth=(self.username, self.password))
        if res.status_code != 200:
            print("Invalid username or password")
            self.username = ""
            self.password = ""
            self.id = 0
            return False

        # If authenticated:
        # Set logged in field to true
        requests.put(self.baseCall + "profile/" + str(self.id) + '/', {'logged_on':True},
                     auth=(self.username, self.password))

        # Pull friends list
        friendsListStr = self.getFriendsList()
        if friendsListStr != '':
            friendIDs = [int(i) for i in friendsListStr.split(',')]
            for user in usersList:
                if user['id'] in friendIDs:
                    self.friends[user['username']] = user['id']

        # return true
        return True


    def logout(self):
        requests.put(self.baseCall + "profile/" + str(self.id) + '/', {'logged_on':False},
                     auth=(self.username, self.password))


    def getFriendsList(self):
        res = requests.get(self.baseCall + "profile/" + str(self.id) + "/", auth=(self.username, self.password))
        return json.loads(res.text)['friends']



    def addFriend(self):
        friendUsername = input("Username of new friend: ")

        if friendUsername in self.friends.keys():
            print("Friend already added\n")
            return

        # Search for friend in database
        res = requests.get(self.baseCall + self.allProfiles).text
        allUsers = json.loads(res)
        for user in allUsers:
            if user['username'] == friendUsername:

                # Add to local friends
                self.friends[friendUsername] = user['id']

                # Update database
                currentFriends = self.getFriendsList()
                if currentFriends == '':
                    requests.put(self.baseCall + "profile/" + str(self.id) + '/',
                                 {'friends': str(user['id'])},
                                 auth=(self.username, self.password))
                else:
                    requests.put(self.baseCall + "profile/" + str(self.id) + '/',
                                 {'friends': currentFriends + ',' + str(user['id'])},
                                 auth=(self.username, self.password))

                # Print confirmation
                print("Friend added\n")
                return

        # If user is not found
        print("User not found\n")


    def checkMessages(self):

        newMessages = []

        # Check for messages where user is the recipient
        res = requests.get(self.baseCall + self.allMessages).text
        messages = json.loads(res)
        for message in messages:
            if message['recipient'] == self.username:
                newMessages.append(message)
        return newMessages


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

for i in user.friends.keys():
    print(i)

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
        newMessages = user.checkMessages()
        print(f"\nYou have {len(newMessages)} new messages\n")
    elif selection == 3:
        user.sendMessage()
    elif selection == 0:
        user.logout()
        break
    else:
        print("Invalid selection.")