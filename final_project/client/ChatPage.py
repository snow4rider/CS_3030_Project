import tkinter as tk
from tkinter import *


# Chat page
class ChatPage(tk.Frame):

    def __init__(self, parent, application, user, activeFriend=""):
        tk.Frame.__init__(self, parent)

        friendsList = list(user.friends.keys())
        if len(friendsList) > 0 and activeFriend == "":
            self.activeFriend = friendsList[0]
        else:
            self.activeFriend = activeFriend

        # Container frames
        chatContainer = tk.Frame(self, bg="SlateGray4")
        chatContainer.pack(side=RIGHT, fill=BOTH, expand=True)
        friendsListContainer = tk.Frame(self, bg="gray25", borderwidth=5)
        friendsListContainer.pack(side=LEFT, fill=Y)

        # Populate friends list
        friendsListFrame = tk.Frame(friendsListContainer, bg="gray30")
        friendsListFrame.pack(fill=BOTH, expand=True, pady=2)
        for friend in friendsList:
            friendButton = Button(friendsListFrame, width=20, text=friend, font=("Whitney", 16, "bold"),
                                  activebackground="gray30", activeforeground="white",
                                  relief=FLAT, bg="gray30", fg="white", cursor="hand2",
                                  command=lambda: self.friend_button_command(application, friend))
            if friend == self.activeFriend:
                friendButton.config(bg="gray50")
            friendButton.pack(padx=5, pady=10)

        # Begin chat window
        chatBoxFrame = tk.Frame(chatContainer, bg="white", relief=SUNKEN)
        chatBoxFrame.pack(fill=BOTH, expand=True, padx=10, pady=10)
        introLabel = Label(chatBoxFrame, text="Chatting with " + self.activeFriend, font=("Whitney", 12), fg="gray")
        introLabel.pack()

        # Submission field
        submissionFrame = tk.Frame(chatContainer, bg="SlateGray4")
        submissionFrame.pack(side=BOTTOM)
        submissionEntry = Entry(submissionFrame, width=72, font=("Whitney", 12))
        submissionEntry.pack(side=LEFT, padx=10, pady=20)
        submissionButton = Button(submissionFrame, text="Submit", font=("Whitney", 12, "bold"))
        submissionButton.pack(side=LEFT, padx=10, pady=20)


    def friend_button_command(self, application, friend):
        self.activeFriend = friend
        application.update_page(ChatPage, friend)
        application.show_page(ChatPage)
