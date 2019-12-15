import json
import requests
import webbrowser


class User:
    def __init__(self):
        # API Calls
        self.baseCall = "http://127.0.0.1:8000/"
        self.ownProfile = ""
        self.allProfiles = "profiles/"
        self.allMessages = "messages/"

        # User info
        self.username = ""
        self.password = ""
        self.id = 0
        self.friends = {}

        # Server info
        self.logged_on = False
        self.active_friend = ""
        self.online_friends = ()

    def register(self):
        webbrowser.open_new(self.baseCall + 'register/')

    def login(self, username, password):
        self.username = username
        self.password = password

        # Authenticate
        res = requests.get(self.baseCall + self.allProfiles)
        usersList = json.loads(res.text)
        for user in usersList:
            if user['username'] == self.username:
                self.id = user['id']
                break
        if self.id == 0:
            self.username = ""
            self.password = ""
            return False
        res = requests.get(self.baseCall + "profile/" + str(self.id) + "/", auth=(self.username, self.password))
        if res.status_code != 200:
            self.username = ""
            self.password = ""
            self.id = 0
            return False

        # If authenticated:
        # Set logged in field to true
        self.ownProfile = "profile/" + str(self.id) + "/"
        requests.put(self.baseCall + self.ownProfile, {'logged_on': True},
                     auth=(self.username, self.password))
        self.logged_on = True

        # Pull friends list
        friendsListStr = self.getFriendsList()
        if friendsListStr != '':
            friendIDs = [int(i) for i in friendsListStr.split(',')]
            for user in usersList:
                if user['id'] in friendIDs:
                    self.friends[user['username']] = user['id']
        self.updateFriendsOnline()

        # return true
        return True

    def logout(self):
        if self.logged_on:
            self.logged_on = False
            requests.put(self.baseCall + self.ownProfile, {'logged_on': False},
                         auth=(self.username, self.password))

    def getFriendsList(self):
        if self.logged_on:
            res = requests.get(self.baseCall + self.ownProfile, auth=(self.username, self.password))
            return json.loads(res.text)['friends']

    def updateFriendsOnline(self):
        if self.logged_on:
            onlineFriends = []
            res = requests.get(self.baseCall + self.allProfiles)
            usersList = json.loads(res.text)
            for user in usersList:
                if user['logged_on'] and user['username'] in self.friends.keys():
                    onlineFriends.append(user['username'])
            self.online_friends = tuple(onlineFriends)

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
                    requests.put(self.baseCall + self.ownProfile,
                                 {'friends': str(user['id'])},
                                 auth=(self.username, self.password))
                else:
                    requests.put(self.baseCall + self.ownProfile,
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

    def sendMessage(self, recipient, message):

        # Get recipient
        if recipient not in self.friends.keys():
            return "Friend not found"

        # Send message
        messageJSON = {
            'text': message,
            'recipient': recipient
        }
        res = requests.post(self.baseCall + self.allMessages, data=messageJSON, auth=(self.username, self.password))
        if res.status_code != 201:
            return "An error occurred: Message not sent."
        else:
            return None
