import tkinter as tk
from tkinter import *
from PIL import Image, ImageTk


# Chat page
class ChatPage(tk.Frame):

    def __init__(self, parent, application, user):
        tk.Frame.__init__(self, parent)

        # Friends list options
        friendsList = list(user.friends.keys())
        if len(friendsList) > 0 and user.active_friend == "":
            user.active_friend = friendsList[0]
        self.onlineIcon = ImageTk.PhotoImage(Image.open(r'media\online.png'))
        self.offlineIcon = ImageTk.PhotoImage(Image.open(r'media\offline.png'))
        self.friendButtons = {}
        self.chatWindows = {}

        # Container frames
        chatContainer = tk.Frame(self, bg="SlateGray4")
        chatContainer.pack(side=RIGHT, fill=BOTH, expand=True)
        friendsListContainer = tk.Frame(self, bg="gray25", borderwidth=5)
        friendsListContainer.pack(side=LEFT, fill=Y)

        # Friends list
        friendsListFrame = tk.Frame(friendsListContainer, bg="gray30")
        friendsListFrame.pack(fill=BOTH, expand=True, pady=2)
        userAddFriendFrame = tk.Frame(friendsListFrame, bg="gray30")
        userAddFriendFrame.pack(fill=X, pady=5)

        # Username
        username = Label(userAddFriendFrame, width=15, text=user.username, font=("Whitney", 16, "bold"), anchor=W,
                         bg="gray30", fg="white")
        username.pack(side=LEFT)

        # Add friend
        img = Image.open(r'media\addFriend.png')
        img = img.resize((32, 32), Image.ANTIALIAS)
        render = ImageTk.PhotoImage(img)
        addFriendIcon = Label(userAddFriendFrame, bg="gray30", image=render)
        addFriendIcon.image = render
        addFriendIcon.pack(side=LEFT)

        # Scroll bar
        friendsScrollBar = Scrollbar(friendsListFrame)
        friendsScrollBar.pack(side=RIGHT, fill=Y)

        # Friend buttons
        for friend in friendsList:

            # Create button
            friendButton = Label(friendsListFrame, width=200, height=50,
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
            friendButton.pack(padx=5, pady=10)
            friendButton.bind("<Button-1>", lambda event, f=friend: self.friend_button_command(user, f))

            # Add to list
            self.friendButtons[friend] = friendButton

            # Chat window
            chatBoxFrame = tk.Frame(chatContainer, bg="white", relief=SUNKEN)
            if friend == user.active_friend:
                chatBoxFrame.pack(fill=BOTH, expand=True, padx=10, pady=10)
            chatScrollBar = Scrollbar(chatBoxFrame)
            chatScrollBar.pack(side=RIGHT, fill=Y)
            introLabel = Label(chatBoxFrame, text="Chatting with " + friend, font=("Whitney", 12), fg="gray")
            introLabel.pack()
            self.chatWindows[friend] = chatBoxFrame

        # Submission field
        submissionFrame = tk.Frame(chatContainer, bg="SlateGray4")
        submissionFrame.pack(side=BOTTOM)
        submissionEntry = Entry(submissionFrame, width=72, font=("Whitney", 12))
        submissionEntry.pack(side=LEFT, padx=10, pady=20)
        submissionEntry.bind("<Return>", lambda event: self.submit_button_command(user, submissionEntry))
        submissionButton = Button(submissionFrame, text="Submit", font=("Whitney", 12, "bold"),
                                  command=lambda: self.submit_button_command(user, submissionEntry))
        submissionButton.pack(side=LEFT, padx=10, pady=20)

    def friend_button_command(self, user, friend):

        # Remove old active friend state
        self.friendButtons[user.active_friend].configure(bg="gray30")
        self.chatWindows[user.active_friend].pack_forget()

        # Set new active friend state
        user.active_friend = friend
        self.friendButtons[friend].configure(bg="gray50")
        self.chatWindows[friend].pack(fill=BOTH, expand=True, padx=10, pady=10)

    def add_friend_button_command(self):
        pass

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

    def update_friends_online(self, user):
        if user.logged_on:
            user.updateFriendsOnline()
            for friend in self.friendButtons.keys():
                if self.friendButtons[friend]['text'] in user.online_friends:
                    self.friendButtons[friend].image = self.onlineIcon
                    self.friendButtons[friend].configure(image=self.onlineIcon)
                else:
                    self.friendButtons[friend].image = self.offlineIcon
                    self.friendButtons[friend].configure(image=self.offlineIcon)
