import tkinter as tk
from tkinter import *
from PIL import Image, ImageTk

from .ChatPage import ChatPage


# Login page
class LoginPage(tk.Frame):

    def __init__(self, parent, application, user):
        tk.Frame.__init__(self, parent)

        # Container frames
        logoUsernameContainer = tk.Frame(self, bg="SlateGray4")
        logoUsernameContainer.pack(fill=BOTH, expand=True)
        passwordButtonContainer = tk.Frame(self, bg="SlateGray4")
        passwordButtonContainer.pack(fill=BOTH, expand=True)

        # App logo
        img = Image.open(r'media\logo.png')
        img = img.resize((400, 200), Image.ANTIALIAS)
        render = ImageTk.PhotoImage(img)
        logo = Label(logoUsernameContainer, width=400, height=200, image=render, bg="SlateGray4")
        logo.image = render
        logo.pack(expand=True)

        # Frames for each field
        usernameFrame = tk.Frame(logoUsernameContainer, bg="SlateGray4")
        usernameFrame.pack(side=BOTTOM)
        passwordFrame = tk.Frame(passwordButtonContainer, bg="SlateGray4")
        passwordFrame.pack(side=TOP)

        # Username field
        usernameTitle = Label(usernameFrame, text='Username', font=("Whitney", 16, "bold"), bg="SlateGray4", fg="white")
        usernameTitle.pack(side=LEFT, padx=10, pady=10)
        usernameEntry = Entry(usernameFrame, font=("Whitney", 16, "bold"))
        usernameEntry.pack(side=LEFT, padx=10, pady=10)

        # Password field
        passwordTitle = Label(passwordFrame, text='Password', font=("Whitney", 16, "bold"), bg="SlateGray4", fg="white")
        passwordTitle.pack(side=LEFT, padx=10, pady=10)
        passwordEntry = Entry(passwordFrame, font=("Whitney", 16, "bold"), show="*")
        passwordEntry.pack(side=LEFT, padx=12, pady=10)

        # Bind enter to login button function
        usernameEntry.bind("<Return>", lambda event: self.login_button_command(user, usernameEntry, passwordEntry,
                                                                         logoUsernameContainer, self, application))
        passwordEntry.bind("<Return>", lambda event: self.login_button_command(user, usernameEntry, passwordEntry,
                                                                         logoUsernameContainer, self, application))
        usernameEntry.focus()

        # Button container
        buttonContainer = tk.Frame(passwordButtonContainer, bg="SlateGray4")
        buttonContainer.pack(pady=10)

        # Register button
        registerButton = Button(buttonContainer, text="Register", font=("Whitney", 16, "bold"),
                                activebackground="SlateGray4", activeforeground="white",
                                relief=FLAT, bg="SlateGray4", fg="white", cursor="hand2",
                                command=lambda: self.register_button_command(user))
        registerButton.pack(side=LEFT, padx=20, pady=5)

        # Login button
        self.failedAttempt = False
        loginButton = Button(buttonContainer, text="Log In", font=("Whitney", 16, "bold"),
                             activebackground="SlateGray4", activeforeground="white",
                             relief=FLAT, bg="SlateGray4", fg="white", cursor="hand2",
                             command=lambda: self.login_button_command(user, usernameEntry, passwordEntry,
                                                                       logoUsernameContainer, self, application))
        loginButton.pack(side=LEFT, padx=20, pady=5)

    def register_button_command(self, user):
        user.register()

    def login_button_command(self, user, usernameEntry, passwordEntry, masterFrame, loginFrame, application):

        # If a field is empty or login fails
        if usernameEntry.get() == "" or passwordEntry.get() == ""\
                or not user.login(usernameEntry.get(), passwordEntry.get()):

            # Empty entry fields
            usernameEntry.delete(0, END)
            passwordEntry.delete(0, END)

            # Display incorrect username or password message
            if not loginFrame.failedAttempt:
                incorrectLabel = Label(masterFrame, text="Username or password incorrect!", font=("Whitney", 12, "bold"),
                                       bg="SlateGray4", fg="red")
                incorrectLabel.pack()
                loginFrame.failedAttempt = True

        # Change to chat page
        else:
            application.update_page((ChatPage))
            application.show_page(ChatPage)
