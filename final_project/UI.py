import tkinter as tk
from tkinter import *
from tkinter import ttk

from client import ClientUser


class Application(tk.Tk):

    def __init__(self, user):
        tk.Tk.__init__(self)
        self.user = user

        # Initialize the size of the whole application, its title, and the little icon
        # that appears at the top left of the window
        self.geometry('1024x512')
        self.title("Chatter")
        self.iconbitmap(r'favicon.ico')

        # Initialize the main content frame
        self.main_window = Frame(self)
        self.main_window.pack(side=TOP, fill=BOTH, expand=True)
        self.main_window.grid_rowconfigure(0, weight=1)
        self.main_window.grid_columnconfigure(0, weight=1)

        # Load each page into a dict
        self.pages = {}
        for page in (LoginPage, ChatPage):
            window = page(self.main_window, user)
            self.pages[page] = window
            window.grid(row=0, column=0, sticky="nsew")

        # Show the login page by default
        self.show_page(LoginPage)

    # Show a page from the page list
    def show_page(self, page):
        active_page = self.pages[page]
        active_page.tkraise()


class FriendsBar:
    def __init__(self, parent, user):
        pass


class LoginPage(tk.Frame):

    def __init__(self, parent, user):
        tk.Frame.__init__(self, parent)

        # Frames for each field
        usernameFrame = tk.Frame(self)
        passWordFrame = tk.Frame(self)

        # Username field
        usernameTitle = Label(self, text='Username', font=("Verdana", 12))
        usernameTitle.pack(side=LEFT)
        usernameEntry = Entry(self)
        usernameEntry.pack(side=LEFT)

        # Password field
        passwordTitle = Label(self, text='Password', font=("Verdana", 12))
        passwordTitle.pack(padx=5, pady=5)
        passwordEntry = Entry(self)
        passwordEntry.pack(padx=5, pady=5)

        # Register button
        registerButton = Button(self, text="Register", font=("Verdana", 12), bg="gray", fg="black",
                                command=lambda: self.register_button_command(user))
        registerButton.pack(padx=5, pady=5)

    def register_button_command(self, user):
        user.register()

    def login_button_command(self, user, username, password):
        user.login(username, password)


class ChatPage(tk.Frame):

    def __init__(self, parent, user):
        tk.Frame.__init__(self, parent)


# Begin application
user = ClientUser()
app = Application(user)
app.mainloop()