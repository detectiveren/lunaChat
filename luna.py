import flet as ft
import settings

# Resources used to develop the app https://flet.dev/docs/tutorials/python-realtime-chat/#getting-started-with-flet

class LunaMessage():
    def __init__(self, lunaUser: str, lunaText: str, lunaMessageType: str):
        self.lunaUser = lunaUser
        self.lunaText = lunaText
        self.lunaMessageType = lunaMessageType # The type of message that is being sent, login message or chat message


def main(page: ft.Page):
    lunaChat = ft.Column()  # Build the layout of the app
    newMessage = ft.TextField()  # Take input from the Text Field
    lunaUsername = ft.TextField(label="Enter your username")

    def onLunaMessage(message: LunaMessage):
        if message.lunaMessageType == "lunaChatMessage":
            lunaChat.controls.append(ft.Text(f"{message.lunaUser}: {message.lunaText}", color=ft.colors.PINK))
        elif message.lunaMessageType == "lunaLoginMessage":
            lunaChat.controls.append(
                ft.Text(message.lunaText, italic=True, color=ft.colors.WHITE, size=12)
            )
        page.update()

    page.pubsub.subscribe(onLunaMessage)

    def sendClick(e):
        # lunaChat.controls.append(ft.Text(newMessage.value))  # Appends the message sent by the user
        page.pubsub.send_all(LunaMessage(lunaUser=page.session.get('lunaUsername'), lunaText=newMessage.value,
                                         lunaMessageType="lunaChatMessage"))
        newMessage.value = ""  # Resets the value
        page.update()  # Updates the page

    def joinClick(e):
        if not lunaUsername.value:
            lunaUsername.error_text = "USERNAME CANNOT BE BLANK"
            lunaUsername.update()
        else:
            page.session.set("lunaUsername", lunaUsername.value)
            page.dialog.open = False
            page.pubsub.send_all(LunaMessage(lunaUser=lunaUsername.value,
                                             lunaText=f"{lunaUsername.value} has joined lunaChat",
                                             lunaMessageType="lunaLoginMessage"))

    page.dialog = ft.AlertDialog(
        open=True,
        modal=True,
        title=ft.Text("Welcome to lunaChat!"),
        content=ft.Column([lunaUsername], tight=True),
        actions=[ft.ElevatedButton(text="Join lunaChat", on_click=joinClick)],
        actions_alignment="end",
    )

    page.add(
        lunaChat, ft.Row(controls=[newMessage, ft.ElevatedButton("Send Luna Message", on_click=sendClick)])
    )


ft.app(main, view=ft.AppView.WEB_BROWSER, host=settings.host, port=settings.port)
