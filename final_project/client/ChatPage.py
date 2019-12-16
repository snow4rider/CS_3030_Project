import tkinter as tk
from tkinter import *
from PIL import Image, ImageTk


# Chat page
class ChatPage(tk.Frame):

    def __init__(self, parent, application, user):
        tk.Frame.__init__(self, parent)
        self.pauseUpdates = False

        # Friends list options
        friendsList = list(user.friends.keys())
        if len(friendsList) > 0 and user.active_friend == "":
            user.active_friend = friendsList[0]
        self.onlineIcon = ImageTk.PhotoImage(Image.open(r'media\online.png'))
        self.offlineIcon = ImageTk.PhotoImage(Image.open(r'media\offline.png'))
        self.friendButtons = {}
        self.chatWindows = {}

        # Container frames
        self.chatContainer = tk.Frame(self, bg="SlateGray4")
        self.chatContainer.pack(side=RIGHT, fill=BOTH, expand=True)
        friendsListContainer = tk.Frame(self, bg="gray25", borderwidth=5)
        friendsListContainer.pack(side=LEFT, fill=Y)

        # Friends list
        self.friendsListFrame = tk.Frame(friendsListContainer, bg="gray30")
        self.friendsListFrame.pack(fill=BOTH, expand=True, pady=2)
        userAddFriendFrame = tk.Frame(self.friendsListFrame, bg="gray30")
        userAddFriendFrame.pack(fill=X, pady=5)

        # Username
        username = Label(userAddFriendFrame, text=user.username, font=("Whitney", 16, "bold"), anchor=W,
                         bg="gray30", fg="white")
        username.pack(side=LEFT)

        # Add friend
        addFriendEntry = Entry(userAddFriendFrame, font=("Whitney", 12), width=20)
        addFriendEntry.pack(side=LEFT, padx=10)
        img = Image.open(r'media\addFriend.png')
        img = img.resize((32, 32), Image.ANTIALIAS)
        render = ImageTk.PhotoImage(img)
        addFriendIcon = Label(userAddFriendFrame, bg="gray30", image=render, cursor="hand2")
        addFriendIcon.image = render
        addFriendIcon.pack(side=RIGHT)
        addFriendEntry.bind("<FocusIn>", lambda event: self.reset_entry_field(addFriendEntry))
        addFriendEntry.bind("<Return>",
                            lambda event: self.add_friend_button_command(user, addFriendEntry.get(), addFriendEntry))
        addFriendIcon.bind("<Button-1>",
                           lambda event: self.add_friend_button_command(user, addFriendEntry.get(), addFriendEntry))

        # Scroll bar
        friendsScrollBar = Scrollbar(self.friendsListFrame)
        friendsScrollBar.pack(side=RIGHT, fill=Y)

        # Friend buttons
        for friend in friendsList:
            self.create_friend(friend, user)

        # Submission field
        submissionFrame = tk.Frame(self.chatContainer, bg="SlateGray4")
        submissionFrame.pack(side=BOTTOM)
        submissionEntry = Entry(submissionFrame, width=65, font=("Whitney", 12))
        submissionEntry.pack(side=LEFT, padx=10, pady=20)
        submissionEntry.bind("<Return>", lambda event: self.submit_button_command(user, submissionEntry))
        submissionButton = Button(submissionFrame, text="Submit", font=("Whitney", 12, "bold"),
                                  command=lambda: self.submit_button_command(user, submissionEntry))
        submissionButton.pack(side=LEFT, padx=10, pady=20)

    # Switch chat view to another friend
    def friend_button_command(self, user, friend):

        # Remove old active friend state
        if user.active_friend != "" and user.active_friend != "0":
            self.friendButtons[user.active_friend].configure(bg="gray30")
            self.chatWindows[user.active_friend].pack_forget()

        # Set new active friend state
        user.active_friend = friend

        # Remove new messages flag and set active
        text = self.friendButtons[friend]['text']
        if text.endswith(" (New Messages)"):
            text = text.replace(" (New Messages)", '')
        self.friendButtons[friend].configure(bg="gray50", text=text)
        self.chatWindows[friend].pack(fill=BOTH, expand=True, padx=10, pady=10)

    # Add a new friend
    def add_friend_button_command(self, user, friend, addFriendEntry=None, makeActive=True):

        # Pause updates
        self.pauseUpdates = True

        # Add friend
        res = user.addFriend(friend)

        # Replace entry with response
        if addFriendEntry is not None:
            addFriendEntry.delete(0, END)
            addFriendEntry.config(fg="red")
            addFriendEntry.insert(0, res)

        # If friend was added
        if res == "Friend added":

            # Create new friend button
            self.create_friend(friend, user)

            # Set new friend as active
            if makeActive:
                self.friend_button_command(user, friend)

        # Resume updates
        self.pauseUpdates = False

    # Create a new button and chat box for a friend
    def create_friend(self, friend, user):
        # Create button
        friendButton = Label(self.friendsListFrame, height=50,
                             text=friend, font=("Whitney", 16, "bold"), anchor=W,
                             image=self.offlineIcon, compound=LEFT,
                             activebackground="gray30", activeforeground="white", bg="gray30", fg="white",
                             relief=FLAT, cursor="hand2")
        if friend in user.online_friends:
            friendButton.configure(image=self.onlineIcon)
            friendButton.image = self.onlineIcon
        else:
            friendButton.image = self.offlineIcon
        if friend == user.active_friend:
            friendButton.config(bg="gray50")
        friendButton.pack(fill=X, padx=5, pady=10)
        friendButton.bind("<Button-1>", lambda event, f=friend: self.friend_button_command(user, f))

        # Add to list
        self.friendButtons[friend] = friendButton

        # Chat window
        chatBoxFrame = tk.Frame(self.chatContainer, bg="white", relief=SUNKEN)
        if friend == user.active_friend:
            chatBoxFrame.pack(fill=BOTH, expand=True, padx=10, pady=10)
        chatScrollBar = Scrollbar(chatBoxFrame)
        chatScrollBar.pack(side=RIGHT, fill=Y)
        introLabel = Label(chatBoxFrame, text="Chatting with " + friend, font=("Whitney", 12), fg="gray")
        introLabel.pack()
        self.chatWindows[friend] = chatBoxFrame

    # Submit a message entry
    def submit_button_command(self, user, entry):

        if entry.get() != "":

            # Create a new text box
            textBox = Frame(self.chatWindows[user.active_friend], bg="white")
            textBox.pack(fill=X)

            # Send message
            res = user.sendMessage(user.active_friend, entry.get())
            if res is None:
                res = entry.get()

                # Show username
                username = Label(textBox, text=user.username + ": ", font=("Whitney", 14, "bold"), fg="blue")
                username.pack(side=LEFT)

            # Show message
            message = Label(textBox, text=res, font=("Whitney", 14), fg="black")
            message.pack(side=LEFT)

            # Clear entry
            entry.delete(0, END)

    # Update online status of friends
    def update_friends_online(self, user):
        if user.logged_on and not self.pauseUpdates:
            user.updateFriendsOnline()
            for friend in self.friendButtons.keys():
                if friend in user.online_friends:
                    self.friendButtons[friend].image = self.onlineIcon
                    self.friendButtons[friend].configure(image=self.onlineIcon)
                else:
                    self.friendButtons[friend].image = self.offlineIcon
                    self.friendButtons[friend].configure(image=self.offlineIcon)

    # Check for new messages
    def update_messages(self, user):
        if user.logged_on and not self.pauseUpdates:
            newMessages = user.checkMessages()
            for message in newMessages:

                # If sender is not in friends list
                if message['sender'] not in user.friends.keys():
                    self.add_friend_button_command(user, message['sender'], makeActive=False)

                # Show new message flag
                currentText = self.friendButtons[message['sender']]['text']
                if not currentText.endswith(" (New Messages)") and user.active_friend != message['sender']:
                    self.friendButtons[message['sender']].config(text=currentText + " (New Messages)")

                # Create a new text box
                textBox = Frame(self.chatWindows[message['sender']], bg="white")
                textBox.pack(fill=X)

                # Show username
                username = Label(textBox, text=message['sender'] + ": ", font=("Whitney", 14, "bold"), fg="red")
                username.pack(side=LEFT)

                # Show message
                newMessage = Label(textBox, text=message['text'], font=("Whitney", 14), fg="black")
                newMessage.pack(side=LEFT)

    # Reset an entry field
    def reset_entry_field(self, entry):
        entry.config(fg="black")
        entry.delete(0, END)
