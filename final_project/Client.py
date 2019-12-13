from client.User import User
from client.UI import Application


# Begin application
user = User()
app = Application(user)
app.mainloop()

# Log user out when program closes
user.logout()