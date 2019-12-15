import tkinter as tk
from tkinter import *
from PIL import Image, ImageTk
import threading, time


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
        self.friendButtons = []

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
        username = Label(userAddFriendFrame, text=user.username, font=("Whitney", 16, "bold"), anchor=W,
                         bg="gray30", fg="white")
        username.pack(side=LEFT)

        # Add friend
        img = Image.open(r'media\addFriend.png')
        img = img.resize((32, 32), Image.ANTIALIAS)
        render = ImageTk.PhotoImage(img)
        addFriendIcon = Label(userAddFriendFrame, bg="gray30", image=render)
        addFriendIcon.image = render
        addFriendIcon.pack(side=RIGHT)

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
            friendButton.bind("<Button-1>", lambda event, f=friend: self.friend_button_command(application, user, f))

            # Add to list
            self.friendButtons.append(friendButton)

        # Chat window
        chatBoxFrame = tk.Frame(chatContainer, bg="white", relief=SUNKEN)
        chatBoxFrame.pack(fill=BOTH, expand=True, padx=10, pady=10)
        chatScrollBar = Scrollbar(chatBoxFrame)
        chatScrollBar.pack(side=RIGHT, fill=Y)
        introLabel = Label(chatBoxFrame, text="Chatting with " + user.active_friend, font=("Whitney", 12), fg="gray")
        introLabel.pack()

        # Submission field
        submissionFrame = tk.Frame(chatContainer, bg="SlateGray4")
        submissionFrame.pack(side=BOTTOM)
        submissionEntry = Entry(submissionFrame, width=72, font=("Whitney", 12))
        submissionEntry.pack(side=LEFT, padx=10, pady=20)
        submissionButton = Button(submissionFrame, text="Submit", font=("Whitney", 12, "bold"))
        submissionButton.pack(side=LEFT, padx=10, pady=20)

    def friend_button_command(self, application, user, friend):
        user.active_friend = friend
        application.update_page(ChatPage)
        application.show_page(ChatPage)

    def add_friend_button_command(self):
        pass

    def update_friends_online(self, user):
        if user.logged_on:
            user.updateFriendsOnline()
            for button in self.friendButtons:
                if button['text'] in user.online_friends:
                    button.image = self.onlineIcon
                    button.configure(image=self.onlineIcon)
                else:
                    button.image = self.offlineIcon
                    button.configure(image=self.offlineIcon)
