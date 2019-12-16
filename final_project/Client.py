from client.User import User
from client.UI import Application, ChatPage
import threading, time


def checkOnlineFriends():
    while not programComplete:
        time.sleep(1)
        app.pages[ChatPage].update_friends_online(user)


def checkMessages():
    while not programComplete:
        time.sleep(1)
        app.pages[ChatPage].update_messages(user)


# Create user and application
user = User()
app = Application(user)

# Start background threads to update from server
programComplete = False
updateFriendsOnlineThread = threading.Thread(target=checkOnlineFriends)
updateFriendsOnlineThread.start()
updateMessagesThread = threading.Thread(target=checkMessages)
updateMessagesThread.start()

# Begin application
app.mainloop()
programComplete = True

# Log user out when program closes
user.logout()