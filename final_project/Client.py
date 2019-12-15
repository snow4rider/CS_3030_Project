from client.User import User
from client.UI import Application, ChatPage
import threading, time


def checkOnlineFriends():
    while True:
        time.sleep(1)
        app.pages[ChatPage].update_friends_online(user)


# Create user and application
user = User()
app = Application(user)

# Start background threads to update from server
updateFriendsOnlineThread = threading.Thread(target=checkOnlineFriends)
updateFriendsOnlineThread.start()

# Begin application
app.mainloop()

# Log user out when program closes
user.logout()