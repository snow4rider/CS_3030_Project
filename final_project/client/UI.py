import tkinter as tk
from tkinter import *

from .LoginPage import LoginPage
from .ChatPage import ChatPage


# Main application window
class Application(tk.Tk):

    def __init__(self, user):
        tk.Tk.__init__(self)
        self.user = user

        # Initialize the size of the whole application, its title, and the little icon
        # that appears at the top left of the window
        self.geometry('1024x512')
        self.title("Chatter")
        self.iconbitmap(r'media\favicon.ico')

        # Initialize the main content frame
        self.main_window = Frame(self, bg="SlateGray4")
        self.main_window.pack(side=TOP, fill=BOTH, expand=True)
        self.main_window.grid_rowconfigure(0, weight=1)
        self.main_window.grid_columnconfigure(0, weight=1)

        # Load each page into a dict
        self.pages = {}
        for page in (LoginPage, ChatPage):
            window = page(self.main_window, self, user)
            self.pages[page] = window
            window.grid(row=0, column=0, sticky="nsew")

        # Show the login page by default
        self.show_page(LoginPage)

    # Show a page from the page list
    def show_page(self, page):
        active_page = self.pages[page]
        active_page.tkraise()

    # Update a page in the application
    def update_page(self, page, activeFriend=None):
        if activeFriend is None:
            window = page(self.main_window, self, self.user)
        else:
            window = page(self.main_window, self, self.user, activeFriend)

        self.pages[page] = window
        window.grid(row=0, column=0, sticky="nsew")
