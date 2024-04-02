import flet as ft
import settings

# Resources used to develop the app https://flet.dev/docs/tutorials/python-realtime-chat/#getting-started-with-flet
# For info on how to deal with keyboard events https://flet.dev/docs/guides/python/keyboard-shortcuts/
# More information for customizing the layout https://flet.dev/docs/tutorials/python-realtime-chat/#animated-scrolling-to-the-last-message

print(f"lunaChat instance {settings.lunaChatName} started on http://{settings.host}:{settings.port}/")


# Moved both getInitials and getAvatarColor outside the previous class as it will be referenced by two classes
# Doesn't need to be within a class anyway


def getInitials(lunaUser: str):
    return lunaUser[:1].capitalize()  # Get the first letter of the username and capitalize it


def getAvatarColor(lunaUser: str):  # Get Avatar colors
    searchForColors = [  # Array of Avatar colors
        ft.colors.AMBER,
        ft.colors.BLUE,
        ft.colors.BROWN,
        ft.colors.CYAN,
        ft.colors.GREEN,
        ft.colors.INDIGO,
        ft.colors.LIME,
        ft.colors.ORANGE,
        ft.colors.PINK,
        ft.colors.PURPLE,
        ft.colors.RED,
        ft.colors.TEAL,
        ft.colors.YELLOW,
    ]
    return searchForColors[hash(lunaUser) % len(searchForColors)]


class LunaMessage():
    def __init__(self, lunaUser: str, lunaText: str, lunaMessageType: str):
        self.lunaUser = lunaUser
        self.lunaText = lunaText
        self.lunaMessageType = lunaMessageType  # The type of message that is being sent, login message or chat message


class lunaChatMessage(ft.Row):
    def __init__(self, message: LunaMessage):
        super().__init__()
        self.vertical_alignment = "start"
        self.controls = [  # This is where the message container is, avatar, username and message are in this container
            ft.CircleAvatar(  # The avatar that will pop up in the message container
                content=ft.Text(getInitials(message.lunaUser)),
                color=ft.colors.WHITE,
                bgcolor=getAvatarColor(message.lunaUser)
            ),
            ft.Column(
                [
                    ft.Text(message.lunaUser, color=ft.colors.PINK),
                    # The username that will pop up in the message container
                    ft.Text(message.lunaText, selectable=True, color=ft.colors.BLUE)
                    # The message that will pop up in the message container
                ],
                tight=True,
                spacing=5

            )
        ]


class lunaImageMessage(ft.Row):
    def __init__(self, imageMessage: LunaMessage):
        super().__init__()
        self.vertical_alignment = "start"
        self.controls = [
            ft.CircleAvatar(  # The avatar that will pop up in the message container
                content=ft.Text(getInitials(imageMessage.lunaUser)),
                color=ft.colors.WHITE,
                bgcolor=getAvatarColor(imageMessage.lunaUser)
            ),
            ft.Column(
                [
                    ft.Text(imageMessage.lunaUser, color=ft.colors.PINK),
                    # The username that will pop up in the message container
                    ft.Text(imageMessage.lunaText, selectable=True, color=ft.colors.BLUE),
                    # The message that will pop up in the message container
                    ft.Image(
                        src=f"{imageMessage.lunaText}",  # The source being the image URL
                        width=512,
                        height=512,
                        fit=ft.ImageFit.CONTAIN,

                    )
                ],
                tight=True,
                spacing=5

            )
        ]


print("loaded classes LunaMessage and LunaChatMessage, message container has been created")

with open('./config/usernamesInUse.txt', 'w') as clearUserList:  # Clear usernameInUse list from the previous session
    clearUserList.write("admin\n")
    clearUserList.close()

print("lunaChat instance is ready")


def main(page: ft.Page):
    lunaChat = ft.ListView(
        expand=True,
        spacing=10,
        auto_scroll=True
    )  # Build the layout of the app
    newMessage = ft.TextField(
        hint_text="Type a message...",
        autofocus=True,
        min_lines=1,
        max_lines=5,
        filled=True,
        expand=True,
    )  # Take input from the Text Field
    currentVersion = "1.0"
    versionBranch = "alpha"
    buildNumber = "2240"
    imageFormats = [".png", ".jpg", ".jpeg", ".gif"]  # Supported image formats
    lunaUsername = ft.TextField(label="Enter your username")

    page.title = "lunaChat"
    page.update()

    print(f"LOG receiving anonymous join on lunaChat instance "
          f"{settings.lunaChatName} ({settings.host}:{settings.port})")

    def onLunaMessage(message: LunaMessage):
        if message.lunaMessageType == "lunaChatMessage":  # If the message type is a chat message
            lunaMsg = lunaChatMessage(message)
        elif message.lunaMessageType == "lunaLoginMessage":  # If the message type is a login message
            lunaMsg = ft.Text(message.lunaText, italic=True, color=ft.colors.WHITE, size=12)
        elif message.lunaMessageType == "lunaImageMessage":  # If the message type is an image message
            lunaMsg = lunaImageMessage(message)
        lunaChat.controls.append(lunaMsg)
        page.update()

    page.pubsub.subscribe(onLunaMessage)  # Updates the web clients when there are new messages

    def lunaBOT(message):
        lunaBOTUsername = "lunaBOT"  # lunaBOT's username
        lunaBOTResponse = "Please enter a parameter when invoking the bot"  # lunaBOT's response

        def sendLunaBOTMessage(response):  # Send the response from lunaBOT into chat
            page.pubsub.send_all(LunaMessage(lunaUser=lunaBOTUsername, lunaText=response,
                                             lunaMessageType="lunaChatMessage"))

        if "buildNumber" in message:  # If the message contains "buildNumber" then lunaBOT will print out the build number
            lunaBOTResponse = f"Build Number: {buildNumber}"  # lunaBOT's response
            sendLunaBOTMessage(lunaBOTResponse)
        if "commands" in message:
            lunaBOTResponse = ("List of commands\n"
                               "buildNumber - Displays lunaChat's build number\n"
                               "birthday - lunaBOT says Happy Birthday\n"
                               "winter - lunaBOT says Happy Winter Holiday\n"
                               "syntax example: !lunaBOT buildNumber")
            sendLunaBOTMessage(lunaBOTResponse)
        if "birthday" in message:
            lunaBOTResponse = "HAPPY BIRTHDAY!"
            sendLunaBOTMessage(lunaBOTResponse)
        if "winter" in message:
            lunaBOTResponse = "HAPPY WINTER HOLIDAY!"
            sendLunaBOTMessage(lunaBOTResponse)
        if "banned_word_sent" in message:
            lunaBOTResponse = f"{lunaUsername.value} tried to send a message that contained a banned word"
            sendLunaBOTMessage(lunaBOTResponse)
        print(f"LOG (Message Type: lunaChatMessage) (lunaBOT): {lunaBOTResponse} (requested by {lunaUsername.value})")

    def sendClick(e):
        # lunaChat.controls.append(ft.Text(newMessage.value))  # Appends the message sent by the user
        with open('./config/bannedWords.txt') as readBannedWords:
            bannedWords = readBannedWords.readlines()  # Read all the usernames from the textfile into the list
            bannedWords = [line.rstrip('\n') for line in bannedWords]

        def standardMessage():
            page.pubsub.send_all(LunaMessage(lunaUser=page.session.get('lunaUsername'), lunaText=newMessage.value,
                                             lunaMessageType="lunaChatMessage"))
            # Grabs the lunaUsername, message and message type

        if "!lunaBOT" in newMessage.value:
            standardMessage()
            lunaBOT(newMessage.value)
        elif any(imgFormat in newMessage.value for imgFormat in imageFormats):  # If the message contains an image link
            print(f"LOG (Message Type: lunaImageMessage) ({lunaUsername.value}) sent an image with a link")
            page.pubsub.send_all(LunaMessage(lunaUser=page.session.get('lunaUsername'), lunaText=newMessage.value,
                                             lunaMessageType="lunaImageMessage"))
        elif newMessage.value.strip() in bannedWords:
            lunaBOT("banned_word_sent")
        else:
            standardMessage()
        print(f"LOG (Message Type: lunaChatMessage) ({lunaUsername.value}): {newMessage.value}")
        # Log the chat messages to the terminal
        newMessage.value = ""  # Resets the value
        page.update()  # Updates the page

    def joinClick(e):
        with open('./config/usernamesInUse.txt') as readUsernames:
            usernamesInUse = readUsernames.readlines()  # Read all the usernames from the textfile into the list
            usernamesInUse = [line.rstrip('\n') for line in usernamesInUse]

        with open('./config/bannedUsernames.txt') as readBannedUsernames:
            bannedUsername = readBannedUsernames.readlines()  # Read all the usernames from the textfile into the list
            bannedUsername = [line.rstrip('\n') for line in bannedUsername]

        if not lunaUsername.value:
            lunaUsername.error_text = "USERNAME CANNOT BE BLANK"
            lunaUsername.update()
        elif "lunaBOT" in lunaUsername.value:  # If the user input is lunaBOT it will return an error
            lunaUsername.error_text = "USERNAME INVALID"
            lunaUsername.update()
            print("LOG (Login System) Anonymous user tried to log in but the username was invalid")
        elif lunaUsername.value.strip() in usernamesInUse:
            # If the username is found in the usernamesInUse list then the username is in use
            lunaUsername.error_text = "USERNAME IN USE"
            lunaUsername.update()
            print(f"LOG (Login System) Anonymous user tried to log in with the username {lunaUsername.value.strip()}"
                  f" but it was already in use")
        elif lunaUsername.value.strip() in bannedUsername:
            lunaUsername.error_text = "USERNAME IS BANNED"
            lunaUsername.update()
            print(f"LOG (Login System) Anonymous user tried to log in with the username {lunaUsername.value.strip()}"
                  f" but the username is banned")
        else:
            page.session.set("lunaUsername", lunaUsername.value)  # Takes in the username value that was entered
            page.dialog.open = False
            page.pubsub.send_all(LunaMessage(lunaUser=lunaUsername.value,
                                             lunaText=f"{lunaUsername.value} has joined {settings.lunaChatName}'s "
                                                      f"lunaChat instance "
                                                      f"({settings.host}:{settings.port})",
                                             lunaMessageType="lunaLoginMessage"))
            print(f"LOG (Message Type: lunaLoginMessage) ({lunaUsername.value}) has joined {settings.lunaChatName}'s "
                  f"lunaChat instance ({settings.host}:{settings.port})")
            # Display the login message in the terminal

            with open('./config/usernamesInUse.txt', 'a') as f:
                f.write(f"{lunaUsername.value}\n")  # Append the username to the list
                f.close()

    def onKeyboard(key: ft.KeyboardEvent):
        if key.key == "Enter":  # If  the key is the Enter key
            sendClick(newMessage.value)  # Send the message that was in the text field

    page.dialog = ft.AlertDialog(
        open=True,
        modal=True,
        title=ft.Text("Welcome to lunaChat!"),
        content=ft.Column([lunaUsername], tight=True),
        actions=[ft.ElevatedButton(text="Join lunaChat", on_click=joinClick, color=ft.colors.PINK)],
        actions_alignment="end",
    )  # Opens the alert dialog welcoming the user to lunaChat and takes the input from the user which is the username

    page.add(ft.Text(f"Version {currentVersion}", size=20, spans=[ft.TextSpan(
        f"{versionBranch}", ft.TextStyle(size=10))]),
             lunaChat, ft.Row(controls=[newMessage,
                                        ft.ElevatedButton("Send lunaMessage", on_click=sendClick,
                                                          color=ft.colors.PINK)]),
             ft.Text(f"Description for {settings.lunaChatName}'s lunaChat instance: {settings.lunaDescription}")
             )
    page.on_keyboard_event = onKeyboard  # Check if there is keyboard input


ft.app(main, assets_dir="assets", view=ft.AppView.WEB_BROWSER, host=settings.host, port=settings.port)
