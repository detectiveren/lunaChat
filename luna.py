import flet as ft
import settings


# Resources used to develop the app https://flet.dev/docs/tutorials/python-realtime-chat/#getting-started-with-flet
# For info on how to deal with keyboard events https://flet.dev/docs/guides/python/keyboard-shortcuts/

class LunaMessage():
    def __init__(self, lunaUser: str, lunaText: str, lunaMessageType: str):
        self.lunaUser = lunaUser
        self.lunaText = lunaText
        self.lunaMessageType = lunaMessageType  # The type of message that is being sent, login message or chat message


def main(page: ft.Page):
    lunaChat = ft.Column()  # Build the layout of the app
    newMessage = ft.TextField()  # Take input from the Text Field
    currentVersion = "1.0"
    versionBranch = "alpha"
    lunaUsername = ft.TextField(label="Enter your username")

    page.title = "lunaChat"
    page.update()

    def onLunaMessage(message: LunaMessage):
        if message.lunaMessageType == "lunaChatMessage":  # If the message type is a chat message
            lunaChat.controls.append(ft.Text(f"{message.lunaUser}: {message.lunaText}", color=ft.colors.PINK))
        elif message.lunaMessageType == "lunaLoginMessage":  # If the message type is a login message
            lunaChat.controls.append(
                ft.Text(message.lunaText, italic=True, color=ft.colors.WHITE, size=12)
            )
        page.update()

    page.pubsub.subscribe(onLunaMessage)  # Updates the web clients when there are new messages

    def sendClick(e):
        # lunaChat.controls.append(ft.Text(newMessage.value))  # Appends the message sent by the user
        page.pubsub.send_all(LunaMessage(lunaUser=page.session.get('lunaUsername'), lunaText=newMessage.value,
                                         lunaMessageType="lunaChatMessage"))  # Grabs the lunaUsername, message and message type
        newMessage.value = ""  # Resets the value
        page.update()  # Updates the page

    def joinClick(e):
        if not lunaUsername.value:
            lunaUsername.error_text = "USERNAME CANNOT BE BLANK"
            lunaUsername.update()
        else:
            page.session.set("lunaUsername", lunaUsername.value)  # Takes in the username value that was entered
            page.dialog.open = False
            page.pubsub.send_all(LunaMessage(lunaUser=lunaUsername.value,
                                             lunaText=f"{lunaUsername.value} has joined {settings.lunaChatName}'s "
                                                      f"lunaChat instance "
                                                      f"({settings.host}:{settings.port})",
                                             lunaMessageType="lunaLoginMessage"))

    def onKeyboard(key: ft.KeyboardEvent):
        if key.key == "Enter":  # If  the key is the Enter key
            sendClick(newMessage.value)  # Send the message that was in the text field

    page.dialog = ft.AlertDialog(
        open=True,
        modal=True,
        title=ft.Text("Welcome to lunaChat!"),
        content=ft.Column([lunaUsername], tight=True),
        actions=[ft.ElevatedButton(text="Join lunaChat", on_click=joinClick)],
        actions_alignment="end",
    )  # Opens the alert dialog welcoming the user to lunaChat and takes the input from the user which is the username

    page.add(
        lunaChat, ft.Row(controls=[newMessage, ft.ElevatedButton("Send lunaMessage", on_click=sendClick)]),
        ft.Text(f"Version {currentVersion}", size=20, spans=[ft.TextSpan(
            f"{versionBranch}", ft.TextStyle(size=10)
        )])
    )
    page.on_keyboard_event = onKeyboard  # Check if there is keyboard input


ft.app(main, assets_dir="assets", view=ft.AppView.WEB_BROWSER, host=settings.host, port=settings.port)
