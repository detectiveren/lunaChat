import flet as ft
import settings
from cryptography.fernet import Fernet
from time import sleep
import sqlite3
import system
import platform


# Resources used to develop the app https://flet.dev/docs/tutorials/python-realtime-chat/#getting-started-with-flet
# For info on how to deal with keyboard events https://flet.dev/docs/guides/python/keyboard-shortcuts/
# More information for customizing the layout 
# https://flet.dev/docs/tutorials/python-realtime-chat/#animated-scrolling-to-the-last-message
# https://flet.dev/docs/controls/page#navigation_bar
# https://flet.dev/docs/controls/appbar/
# https://flet.dev/docs/controls/banner/


def lunaChatInfo():
    """Information about the application"""
    # This code is a work in progress
    lunaInfo = system.getLunaChatInfo("Version")
    lunaPlatformsSupported = system.getLunaChatInfo("hostPlatforms")
    lunaVersion = lunaInfo[0]
    lunaBranch = lunaInfo[2]
    supportedWindowsPlatforms = lunaPlatformsSupported[0][1]
    if platform.system() == "Windows":
        if platform.release() < supportedWindowsPlatforms:
            print(f"This version of Windows is unsupported in lunaChat {lunaVersion}, please upgrade to Windows "
                  + supportedWindowsPlatforms + " or later")
            input("Press any key to continue...")
            exit()
    return lunaInfo


lunaChatInfo()
systemInfoMessage = lunaChatInfo()
print(f"lunaChat {systemInfoMessage[0]} {systemInfoMessage[2]} Build {systemInfoMessage[3]}")

print(f"lunaChat instance {settings.lunaChatName} started on http://{settings.host}:{settings.port}/")


# Moved both getInitials and getAvatarColor outside the previous class as it will be referenced by two classes
# Doesn't need to be within a class anyway


# THIS ENCRYPTION METHOD IS GOING TO BE REPLACED BY ANOTHER ONE
def fernetEncryptMessage(message):  # Grab the message from the user
    key = Fernet.generate_key()  # Generate a key
    text = Fernet(key)  # Initialize Fernet with the generated key
    encoded_message = message.encode()  # Encode the message
    encrypted_message = text.encrypt(encoded_message)  # Encrypt the message
    return encrypted_message, text
    # Return the encrypted message alongside the key


# THIS ENCRYPTION METHOD IS GOING TO BE REPLACED BY ANOTHER ONE
def fernetDecryptMessage(message, key):  # Grab the encrypted message and key
    decrypted_message = key.decrypt(message)  # Decrypt the message using the key
    decoded_message = decrypted_message.decode()  # Decode the message
    return decoded_message
    # Return the decrypted message


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


# Where the colors of UI elements are defined
if settings.lunaExperimentalColorOverride:
    chatMessageColor = ft.colors.BLACK
    UsernameColor = ft.colors.BLACK
    messageBoxColor = ft.colors.WHITE
    messageTypeColor = ft.colors.BLACK
    titleTextColor = ft.colors.BLACK
    descriptionTextColor = ft.colors.BLACK
    dialogColor = ft.colors.PINK_50
    dialogButtonColor = ft.colors.PINK_100
    dialogMessageBoxColor = ft.colors.WHITE
    pageBackgroundColor = ft.colors.PINK_50
    loginMessageColor = ft.colors.BLACK
    bannerBackgroundColor = ft.colors.PINK_100
    bannerTextColor = ft.colors.BLACK
    bannerIconColor = ft.colors.BLACK
    bannerButtonColor = ft.colors.PINK_50
    bannerButtonTextColor = ft.colors.BLACK
else:
    chatMessageColor = ft.colors.BLUE
    UsernameColor = ft.colors.PINK
    messageBoxColor = ft.colors.GREY_900
    messageTypeColor = ft.colors.WHITE
    titleTextColor = ft.colors.WHITE
    descriptionTextColor = ft.colors.WHITE
    dialogColor = ft.colors.GREY_900
    dialogButtonColor = ft.colors.GREY_900
    dialogMessageBoxColor = ft.colors.GREY_800
    pageBackgroundColor = ft.colors.BLACK
    loginMessageColor = ft.colors.WHITE
    bannerBackgroundColor = ft.colors.PINK_700
    bannerTextColor = ft.colors.WHITE
    bannerIconColor = ft.colors.WHITE
    bannerButtonColor = ft.colors.PINK_100
    bannerButtonTextColor = ft.colors.PINK


class LunaMessage():
    def __init__(self, lunaUser: str, lunaText: str, lunaMessageType: str, lunaKey):
        """The main attributes of a message"""
        self.lunaUser = lunaUser
        self.lunaText = lunaText
        self.lunaMessageType = lunaMessageType  # The type of message that is being sent, login message or chat message
        self.lunaKey = lunaKey  # The message key


class lunaChatMessage(ft.Row):
    def __init__(self, message: LunaMessage):
        """The layout of the user message including the user avatar and message"""
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
                    ft.Text(message.lunaUser, color=UsernameColor),
                    # The username that will pop up in the message container
                    ft.Text(message.lunaText, selectable=True)
                    # The message that will pop up in the message container
                ],
                tight=True,
                spacing=5

            )
        ]


class lunaImageMessage(ft.Row):
    def __init__(self, imageMessage: LunaMessage):
        """The layout of the user message including the user avatar, image and message"""
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


class lunaVideoMessage(ft.Row):
    # This does not work at the moment
    def __init__(self, videoMessage: LunaMessage):
        super().__init__()

        # def play_or_pause(e):
        #    video.play_or_pause()

        videoEmbed = [
            ft.VideoMedia(
                f"{videoMessage.lunaText}"
            )
        ]
        self.vertical_alignment = "start"
        self.controls = [
            ft.CircleAvatar(  # The avatar that will pop up in the message container
                content=ft.Text(getInitials(videoMessage.lunaUser)),
                color=ft.colors.WHITE,
                bgcolor=getAvatarColor(videoMessage.lunaUser)
            ),
            ft.Column(
                [
                    ft.Text(videoMessage.lunaUser, color=ft.colors.PINK),
                    # The username that will pop up in the message container
                    ft.Text(videoMessage.lunaText, selectable=True, color=ft.colors.BLUE),
                    # The message that will pop up in the message container
                    ft.Video(
                        expand=True,
                        playlist=videoEmbed,
                        playlist_mode=ft.PlaylistMode.LOOP,
                        fill_color=ft.colors.BLUE_400,
                        aspect_ratio=16 / 9,
                        volume=100,
                        autoplay=True,
                        filter_quality=ft.FilterQuality.HIGH,
                        muted=False
                    ),
                ],
                tight=True,
                spacing=5

            )
        ]


def testDatabase():
    """Test the integrity of the database"""
    database_connection = sqlite3.connect('lunaData.db')  # Establish connection to the database

    database_cursor = database_connection.cursor()  # Create the cursor

    database_cursor.execute('PRAGMA integrity_check;')  # Runs an integrity check

    result = database_cursor.fetchone()  # Catch the result

    if result[0] == "ok":
        dbIntegrityResult = "Database Integrity completed with no errors"
        print(dbIntegrityResult)
    else:
        dbIntegrityResult = (f"Database Integrity Check failed. Please shut down the application and repair or replace "
                             f"the database before relaunching. \nDatabase Integrity Error: {result[0]}")
        print(dbIntegrityResult)
    return dbIntegrityResult


if settings.testDatabaseIntegrityOnLaunch:
    testDatabase()

with open('./config/usernamesInUse.txt', 'w') as clearUserList:  # Clear usernameInUse list from the previous session
    clearUserList.write("admin\n")
    clearUserList.close()

print("lunaChat instance is ready")


def main(page: ft.Page):
    if settings.lunaExperimentalColorOverride:
        page.theme_mode = 'light'
        page.update()
    else:
        page.theme_mode = 'dark'
        page.update()

    def onLunaChatLog(topic, chatLog: LunaMessage):
        """Adds previous chat log messages to the chat"""
        if chatLog.lunaMessageType == "lunaChatMessage":  # If the message type is a chat message
            # decrypted_message = fernetDecryptMessage(chatLog.lunaText, chatLog.lunaKey)  # Decrypt the message
            message = LunaMessage(lunaUser=chatLog.lunaUser, lunaText=chatLog.lunaText,
                                  lunaMessageType=chatLog.lunaMessageType, lunaKey=chatLog.lunaKey)
            # Add the decrypted message to LunaMessage
            lunaMsg = lunaChatMessage(message)

        lunaChat.controls.append(lunaMsg)
        page.update()

    def onLunaMessage(topic, message: LunaMessage):
        """Adds the message to the onLunaMessage topic which adds it to chat"""
        if message.lunaMessageType == "lunaChatMessage":  # If the message type is a chat message
            # decrypted_message = fernetDecryptMessage(message.lunaText, message.lunaKey)  # Decrypt the message
            message = LunaMessage(lunaUser=message.lunaUser, lunaText=message.lunaText,
                                  lunaMessageType=message.lunaMessageType, lunaKey=message.lunaKey)
            # Add the decrypted message to LunaMessage
            lunaMsg = lunaChatMessage(message)
        elif message.lunaMessageType == "lunaLoginMessage":  # If the message type is a login message
            lunaMsg = ft.Text(message.lunaText, italic=True, color=loginMessageColor, size=12)
        elif message.lunaMessageType == "lunaImageMessage":  # If the message type is an image message
            # decrypted_message = fernetDecryptMessage(message.lunaText, message.lunaKey)
            message = LunaMessage(lunaUser=message.lunaUser, lunaText=message.lunaText,
                                  lunaMessageType=message.lunaMessageType, lunaKey=message.lunaKey)
            lunaMsg = lunaImageMessage(message)
        elif message.lunaMessageType == "lunaVideoMessage":
            # decrypted_message = fernetDecryptMessage(message.lunaText, message.lunaKey)
            message = LunaMessage(lunaUser=message.lunaUser, lunaText=message.lunaText,
                                  lunaMessageType=message.lunaMessageType, lunaKey=message.lunaKey)
            lunaMsg = lunaVideoMessage(message)

        lunaChat.controls.append(lunaMsg)
        page.update()

    page.pubsub.subscribe(onLunaMessage)  # Updates the web clients when there are new messages

    # Function for lunaBOT
    def lunaBOT(message):
        """Handles lunaBOT's responses to user requests"""
        lunaBOTUsername = "lunaBOT"  # lunaBOT's username
        lunaBOTResponse = "Please enter a parameter when invoking the bot"  # lunaBOT's response

        def sendLunaBOTMessage(response):  # Send the response from lunaBOT into chat
            """Sends lunaBOT's message to chat"""
            # encrypted_bot_message, bot_key = fernetEncryptMessage(response)  # Encrypt the bots messages
            page.pubsub.send_all_on_topic("Default", LunaMessage(lunaUser=lunaBOTUsername, lunaText=response,
                                                                 lunaMessageType="lunaChatMessage", lunaKey=0))

        if message == "!lunaBOT":
            lunaBOTResponse = f"Please enter a parameter when invoking the bot (requested by {lunaUserStorage.value})"
            sendLunaBOTMessage(lunaBOTResponse)
        if "buildNumber" in message:  # If the message contains "buildNumber" then lunaBOT will print out the build number
            lunaBOTResponse = f"Build {buildNumber}"  # lunaBOT's response
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
            lunaBOTResponse = f"{lunaUserStorage.value} tried to send a message that contained a banned word"
            sendLunaBOTMessage(lunaBOTResponse)
        if "versionInfo" in message:
            lunaBOTResponse = f"lunaChat 1.0\nAlpha 3\nBuild {buildNumber}"
            sendLunaBOTMessage(lunaBOTResponse)
        if "ban" in message:
            messageSplit = message.split()
            username = messageSplit[2]
            print(username)  # Not complete
        if "dbCheck" in message:
            lunaBOTResponse = f"{str(testDatabase())}"
            sendLunaBOTMessage(lunaBOTResponse)

        # Sends the lunaUsername, message, message type and message key
        conn = sqlite3.connect('lunaData.db')
        cursor = conn.cursor()

        try:
            # Check if the username and password match an existing account
            cursor.execute("SELECT id FROM accounts WHERE username = ?",
                           (lunaBOTUsername,))
            grabUserID = cursor.fetchone()
            userID = grabUserID[0]

            cursor.execute("INSERT INTO messages (user_id, message, key) VALUES (?, ?, ?)",
                           (userID, lunaBOTResponse, 0))
            conn.commit()

        except sqlite3.Error as e:
            print("Error:", e)

        print(
            f"LOG (Message Type: lunaChatMessage) (lunaBOT): {lunaBOTResponse} (requested by {lunaUserStorage.value})")

    # Function for checking if the server password is correct
    def passwordCheck(e):
        """Takes the input from the password textfield and checks if it's the correct password"""
        if lunaServerPassword.value == settings.serverPassword:
            page.session.set("lunaServerPassword", lunaServerPassword.value)
            page.close = True
            if settings.enableAccountCreation:  # Calls the login dialog once it has closed the password dialog
                displayLoginHub()
            else:
                displayLoginHubRegisterDisabled()
            lunaErrorText.color = ft.colors.WHITE
            lunaErrorText.value = "Please enter a username and password"
            lunaErrorText.update()
        else:
            lunaErrorText.color = ft.colors.RED
            lunaErrorText.value = "INVALID PASSWORD"
            lunaErrorText.update()

    def createLunaChatAccount(e):
        """Handles the creation of a user account"""
        if not lunaUsername.value or not lunaPassword.value:
            if not lunaUsername.value:
                lunaErrorText.color = ft.colors.RED
                lunaErrorText.value = "Please enter a username"
                lunaErrorText.update()
            if not lunaPassword.value:
                lunaErrorText.color = ft.colors.RED
                lunaErrorText.value = "Please enter a password"
                lunaErrorText.update()
        else:
            conn = sqlite3.connect('lunaData.db')

            cursor = conn.cursor()

            lunaUsername.value = lunaUsername.value.strip()

            # Add the account to the records
            try:
                # Check if the username is unique
                cursor.execute("SELECT id FROM accounts WHERE username = ?", (lunaUsername.value,))
                result = cursor.fetchone()

                if result:
                    lunaUsername.error_text = "Username already exists"
                    lunaUsername.update()
                else:
                    lunaUsername.error_text = ""
                    lunaUsername.update()
                    # Insert the new account without specifying the ID
                    cursor.execute("INSERT INTO accounts (username, password, status) VALUES (?, ?, ?)",
                                   (lunaUsername.value, lunaPassword.value, 0))
                    conn.commit()
                    print("LOG account created successfully with ID:", cursor.lastrowid)
                    lunaUsername.value = ""
                    lunaPassword.value = ""
                    accountCreatedSuccessfullyScreen()
            except sqlite3.Error as e:
                print("Error:", e)
            finally:
                # Close the connection
                conn.close()

    def deleteLunaAccount(e):
        """Handles the deletion of a user account"""
        if not lunaPassword.value:
            lunaErrorText.color = ft.colors.RED
            lunaErrorText.value = "Please enter a password"
            lunaErrorText.update()
        else:
            conn = sqlite3.connect('lunaData.db')

            cursor = conn.cursor()

            lunaUserStorage.value = lunaUserStorage.value.strip()

            lunaDeleteUser = lunaUserStorage.value

            # Add the account to the records
            try:
                # Check if the username is unique
                cursor.execute("SELECT id FROM accounts WHERE username = ? AND password = ?", (lunaDeleteUser,
                                                                                               lunaPassword.value))
                result = cursor.fetchone()

                if result:
                    lunaErrorText.value = "Account has been deleted"
                    lunaErrorText.update()
                    logOutLunaChat("")
                    print(result)
                    cursor.execute("DELETE FROM messages WHERE user_id = ?", (result[0],))
                    cursor.execute("DELETE FROM reports WHERE user_id = ?", (result[0],))
                    cursor.execute("DELETE FROM roles WHERE user_id = ?", (result[0],))
                    cursor.execute("DELETE FROM accounts WHERE username = ?", (lunaDeleteUser,))
                    conn.commit()
                    print("LOG account deleted successfully with username:", lunaUserStorage.value)
                    lunaUsername.value = ""
                    lunaPassword.value = ""
                else:
                    lunaErrorText.color = ft.colors.RED
                    lunaErrorText.value = "The password you entered is incorrect"
                    lunaErrorText.update()
            except sqlite3.Error as e:
                print("Error:", e)
            finally:
                # Close the connection
                conn.close()

    def changeUserPassword(e):
        """Handles changing a user's password"""
        if not lunaPassword.value:
            lunaErrorText.color = ft.colors.RED
            lunaErrorText.value = "Please enter a password"
            lunaErrorText.update()
        else:
            conn = sqlite3.connect('lunaData.db')

            cursor = conn.cursor()

            lunaCurrentPassword = lunaPassword.value

            try:
                # Check if the username and password match an existing account
                cursor.execute("SELECT id FROM accounts WHERE username = ? AND password = ?",
                               (lunaUserStorage.value, lunaCurrentPassword))

                grabUserID = cursor.fetchone()

                if grabUserID:
                    userID = grabUserID[0]

                    cursor.execute("UPDATE accounts SET password = ? WHERE id = ?",
                                   (lunaChangePassword.value, userID))
                    conn.commit()

                    print("LOG account changed password successfully with username:", lunaUserStorage.value)

                    logOutLunaChat("")
                else:
                    lunaErrorText.color = ft.colors.RED
                    lunaErrorText.value = "The old password you entered is incorrect"
                    lunaErrorText.update()

            except sqlite3.Error as e:
                print("Error:", e)
            finally:
                # Close the connection
                conn.close()

    def changeUserStatus(e):
        """Handles the user changing their status"""
        print("Testing User Status Function")
        # Sends the lunaUsername, message, message type and message key
        conn = sqlite3.connect('lunaData.db')
        cursor = conn.cursor()

        lunaStatusStorage.value = lunaStatus.value
        lunaStatus.value = ""

        try:
            # Check if the username and password match an existing account
            cursor.execute("SELECT id FROM accounts WHERE username = ? AND password = ?",
                           (lunaUserStorage.value, lunaPassStorage.value))
            grabUserID = cursor.fetchone()
            userID = grabUserID[0]

            cursor.execute("UPDATE accounts SET customStatusMessage = ? WHERE id = ?",
                           (lunaStatusStorage.value, userID))
            conn.commit()

        except sqlite3.Error as e:
            print("Error:", e)

    def backToLoginHub(e):
        """Sends the user back to the Login Hub"""
        page.close = True
        lunaErrorText.color = ft.colors.WHITE
        lunaErrorText.value = "Please enter a username and password"
        if settings.enableAccountCreation:
            displayLoginHub()
        else:
            displayLoginHubRegisterDisabled()

    def loginMenu(e):
        """Closes the prior dialog and opens Login Menu dialog"""
        page.close = True
        loginDialog()

    def registerMenu(e):
        """Closes the prior dialog and opens Register Menu dialog"""
        page.close = True
        registerDialog()

    def accountCreatedSuccessfullyScreen():
        """Closes the prior dialog and opens Account Created Successfully Screen dialog"""
        page.close = True
        displayAccountCreated()

    def deleteAccountMenu(e):
        """Closes the prior dialog and opens Delete Account Screen dialog"""
        page.close = True
        deleteAccountDialog()

    def changePasswordMenu(e):
        """Closes the prior dialog and opens Change Password Screen dialog"""
        page.close = True
        changePasswordDialog()

    def closeDeleteAccountDialog(e):
        """Closes the Delete Account dialog"""
        deleteAccount.open = False
        page.update()

    def closeChangePasswordDialog(e):
        """Closes the Change Password dialog"""
        changePassword.open = False
        page.update()

    def retrieveChatLogs():
        """Retrieves the chat logs from the database"""
        # Sends the lunaUsername, message, message type and message key
        page.pubsub.unsubscribe()
        page.pubsub.subscribe_topic("ChatLogs", onLunaChatLog)
        conn = sqlite3.connect('lunaData.db')
        cursor = conn.cursor()

        try:
            # Check if the username and password match an existing account
            cursor.execute("SELECT user_id, message FROM messages")
            grabMessageDetails = cursor.fetchall()
            # print(grabMessageDetails)

            # Loop through each row in the results and print the user ID and message
            for row in grabMessageDetails:
                userID = row[0]
                message = row[1]
                cursor.execute("SELECT username FROM accounts WHERE id = ?", (userID,))
                grabUsername = cursor.fetchone()
                username = grabUsername[0]
                # encrypted_message, key = fernetEncryptMessage(message)
                # Encrypt the message and return both the encrypted message and key
                page.pubsub.send_all_on_topic("ChatLogs", LunaMessage(lunaUser=username, lunaText=message,
                                                                      lunaMessageType="lunaChatMessage", lunaKey=0))

            conn.close()

        except sqlite3.Error as e:
            print("Error:", e)

        page.pubsub.unsubscribe_topic("ChatLogs")
        page.pubsub.subscribe_topic("Default", onLunaMessage)

    def lunaSearchQuery(e):
        lunaUserProfileStorage.value = lunaSearch.value
        lunaSearch.value = ""

        conn = sqlite3.connect('lunaData.db')
        cursor = conn.cursor()

        try:
            # Check if the username and password match an existing account
            cursor.execute("SELECT username FROM accounts WHERE username = ?",
                           (lunaUserProfileStorage.value,))
            grabUsername = cursor.fetchone()

            if grabUsername:
                username = grabUsername[0]

                cursor.execute("SELECT customStatusMessage FROM accounts WHERE username = ?",
                               (username,))

                fetchUserStatus = cursor.fetchone()

                customStatusMessage = fetchUserStatus[0]

                if str(customStatusMessage) == "None":
                    lunaUserProfileStatusStorage.value = f"No status set by {username}"
                else:
                    lunaUserProfileStatusStorage.value = str(customStatusMessage)

                page.go(f"/profile/{lunaUserProfileStorage.value}")

        except sqlite3.Error as e:
            print("Error:", e)


    # Function for when a user sends a message
    def sendClick(e):
        """Handles the message that was sent by the user"""

        emptyMsg = False
        # lunaChat.controls.append(ft.Text(newMessage.value))  # Appends the message sent by the user
        with open('./config/bannedWords.txt') as readBannedWords:
            bannedWords = readBannedWords.readlines()  # Read all the usernames from the textfile into the list
            bannedWords = [line.rstrip('\n') for line in bannedWords]

        # message = newMessage.value  # This is the message in plain text so that the if statements can read it
        # encrypted_message, key = fernetEncryptMessage(newMessage.value)
        # Encrypt the message and return both the encrypted message and key (ENCRYPTION OFF)
        # newMessage.value = encrypted_message

        # Put the encrypted message into newMessage.value

        def standardMessage():
            """Sends a standard message to chat"""
            page.pubsub.send_all_on_topic("Default", LunaMessage(lunaUser=page.session.get('lunaUsername'),
                                                                 lunaText=newMessage.value,
                                                                 lunaMessageType="lunaChatMessage", lunaKey=0))
            # Sends the lunaUsername, message, message type and message key
            conn = sqlite3.connect('lunaData.db')
            cursor = conn.cursor()

            try:
                # Check if the username and password match an existing account
                cursor.execute("SELECT id FROM accounts WHERE username = ? AND password = ?",
                               (lunaUserStorage.value, lunaPassStorage.value))
                grabUserID = cursor.fetchone()
                userID = grabUserID[0]

                cursor.execute("INSERT INTO messages (user_id, message, key) VALUES (?, ?, ?)",
                               (userID, newMessage.value, 0))
                conn.commit()

            except sqlite3.Error as e:
                print("Error:", e)

        if "!lunaBOT" in newMessage.value:
            standardMessage()
            lunaBOT(newMessage.value)
        elif any(imgFormat in newMessage.value for imgFormat in imageFormats):  # If the message contains an image link
            print(f"LOG (Message Type: lunaImageMessage) ({lunaUserStorage.value}) sent an image with a link")
            page.pubsub.send_all_on_topic("Default", LunaMessage(lunaUser=page.session.get('lunaUsername'),
                                                                 lunaText=newMessage.value,
                                                                 lunaMessageType="lunaImageMessage", lunaKey=0))
        # elif any(videoFormat in message for videoFormat in videoFormats):
        #    print(f"LOG (Message Type: lunaVideoMessage) ({lunaUsername.value}) sent a video with a link")
        #    page.pubsub.send_all(LunaMessage(lunaUser=page.session.get('lunaUsername'), lunaText=newMessage.value,
        #                                     lunaMessageType="lunaVideoMessage", lunaKey=key))
        elif newMessage.value.strip() in bannedWords:
            lunaBOT("banned_word_sent")
        elif newMessage.value.strip() == "":
            newMessage.error_text = "MESSAGE CANNOT BE EMPTY"
            newMessage.value = ""  # Reset the message value
            newMessage.update()  # Update the message box
            sleep(5)  # Wait 5 seconds before changing the message box back to normal
            newMessage.error_text = ""  # Clear out the error text
            emptyMsg = True
        else:
            standardMessage()
        if not emptyMsg:  # If the message was not empty
            print(f"LOG (Message Type: lunaChatMessage) ({lunaUserStorage.value}): {newMessage.value}")
        # Log the chat messages to the terminal
        newMessage.value = ""  # Resets the value
        page.update()  # Updates the page

    def joinClick(e):
        """Handles the logging into account process"""
        with open('./config/usernamesInUse.txt') as readUsernames:
            usernamesInUse = readUsernames.readlines()  # Read all the usernames from the textfile into the list
            usernamesInUse = [line.rstrip('\n') for line in usernamesInUse]

        with open('./config/bannedUsernames.txt') as readBannedUsernames:
            bannedUsername = readBannedUsernames.readlines()  # Read all the usernames from the textfile into the list
            bannedUsername = [line.rstrip('\n') for line in bannedUsername]

        if not lunaUsername.value:
            lunaErrorText.color = ft.colors.RED
            lunaErrorText.value = "USERNAME CANNOT BE BLANK"
            lunaErrorText.update()
            lunaUsername.value = ""
        elif "lunaBOT" in lunaUsername.value:  # If the user input is lunaBOT it will return an error
            lunaErrorText.color = ft.colors.RED
            lunaErrorText.value = "USERNAME INVALID"
            lunaErrorText.update()
            lunaUsername.value = ""
            print("LOG (Login System) Anonymous user tried to log in but the username was invalid")
        elif lunaUsername.value.strip() in usernamesInUse:
            # If the username is found in the usernamesInUse list then the username is in use
            lunaErrorText.color = ft.colors.RED
            lunaErrorText.value = "USERNAME IN USE"
            lunaErrorText.update()
            print(f"LOG (Login System) Anonymous user tried to log in with the username {lunaUsername.value.strip()}"
                  f" but it was already in use")
            lunaUsername.value = ""
        elif lunaUsername.value.strip() in bannedUsername:
            lunaErrorText.color = ft.colors.RED
            lunaErrorText.value = "USERNAME IS BANNED"
            lunaErrorText.update()
            print(f"LOG (Login System) Anonymous user tried to log in with the username {lunaUsername.value.strip()}"
                  f" but the username is banned")
            lunaUsername.value = ""
        else:
            conn = sqlite3.connect('lunaData.db')
            cursor = conn.cursor()

            try:
                # Check if the username and password match an existing account
                cursor.execute("SELECT id FROM accounts WHERE username = ? AND password = ?",
                               (lunaUsername.value, lunaPassword.value))
                result = cursor.fetchone()

                if result:
                    lunaUserStorage.value = lunaUsername.value
                    lunaUsername.value = ""
                    lunaPassStorage.value = lunaPassword.value
                    lunaPassword.value = ""
                    print(f"LOG {lunaUserStorage.value} has logged in")
                    # Optionally, you can update the UI to reflect the successful login
                    # Add your post-login logic here (e.g., redirect to chat interface)
                    page.session.set("lunaUsername",
                                     lunaUserStorage.value)  # Takes in the username value that was entered
                    page.close = True

                    userID = result[0]

                    cursor.execute("SELECT customStatusMessage FROM accounts WHERE id = ?",
                                   (userID,))

                    fetchUserStatus = cursor.fetchone()

                    customStatusMessage = fetchUserStatus[0]
                    lunaStatus.value = customStatusMessage
                    if settings.displayServerAddressOnLogin:  # If the value is true then display the server address and port
                        page.pubsub.send_all_on_topic("Default", LunaMessage(lunaUser=lunaUserStorage.value,
                                                                             lunaText=f"{lunaUserStorage.value} has joined {settings.lunaChatName}'s lunaChat instance "
                                                                                      f"({settings.host}:{settings.port})",
                                                                             lunaMessageType="lunaLoginMessage",
                                                                             lunaKey=0))
                    else:
                        page.pubsub.send_all_on_topic("Default", LunaMessage(lunaUser=lunaUserStorage.value,
                                                                             lunaText=f"{lunaUserStorage.value} has joined {settings.lunaChatName}'s lunaChat instance",
                                                                             lunaMessageType="lunaLoginMessage",
                                                                             lunaKey=0))
                    page.go(f'/{settings.chatPortalName}')
                    print(
                        f"LOG (Message Type: lunaLoginMessage) ({lunaUserStorage.value}) has joined {settings.lunaChatName}'s "
                        f"lunaChat instance ({settings.host}:{settings.port})")
                    # Display the login message in the terminal
                    retrieveChatLogs()

                    with open('./config/usernamesInUse.txt', 'a') as f:
                        f.write(f"{lunaUserStorage.value}\n")  # Append the username to the list
                        f.close()
                else:
                    lunaErrorText.color = ft.colors.RED
                    lunaErrorText.value = "Invalid username or password"
                    lunaErrorText.update()
            except sqlite3.Error as e:
                print("Error:", e)
            finally:
                # Close the connection
                conn.close()

    lunaChat = ft.ListView(
        expand=True,
        spacing=10,
        auto_scroll=True
    )  # Build the layout of the app
    newMessage = ft.CupertinoTextField(
        placeholder_text="Type a message...",
        placeholder_style=ft.TextStyle(size=15, color=messageTypeColor),
        color=messageTypeColor,
        autofocus=True,
        bgcolor=messageBoxColor,
        min_lines=1,
        max_lines=5,
        filled=True,
        expand=True,
        on_submit=sendClick,
        shift_enter=True,
    )  # Take input from the Text Fields
    grabLunaInfo = lunaChatInfo()
    currentVersion = grabLunaInfo[0]
    versionBranch = grabLunaInfo[2]
    buildNumber = grabLunaInfo[3]
    imageFormats = [".png", ".jpg", ".jpeg", ".gif"]  # Supported image formats
    videoFormats = [".mp4"]
    lunaUsername = ft.CupertinoTextField(placeholder_text="Enter your username", color=messageTypeColor,
                                         bgcolor=dialogMessageBoxColor,
                                         placeholder_style=ft.TextStyle(size=15, color=messageTypeColor),
                                         on_submit=joinClick)
    lunaPassword = ft.CupertinoTextField(placeholder_text="Enter your password", color=messageTypeColor,
                                         bgcolor=dialogMessageBoxColor,
                                         placeholder_style=ft.TextStyle(size=15, color=messageTypeColor),
                                         on_submit=joinClick,
                                         password=True,
                                         can_reveal_password=True)
    lunaChangePassword = ft.CupertinoTextField(placeholder_text="Enter your new password", color=messageTypeColor,
                                               bgcolor=dialogMessageBoxColor,
                                               placeholder_style=ft.TextStyle(size=15, color=messageTypeColor),
                                               on_submit=joinClick,
                                               password=True,
                                               can_reveal_password=True)
    lunaUserStorage = ft.Text("")
    lunaPassStorage = ft.Text("")
    lunaStatusStorage = ft.Text("")
    lunaServerPassword = ft.CupertinoTextField(placeholder_text="Enter password", color=messageTypeColor,
                                               bgcolor=dialogMessageBoxColor,
                                               placeholder_style=ft.TextStyle(size=15, color=messageTypeColor),
                                               on_submit=passwordCheck, password=True, can_reveal_password=True)
    lunaUserProfileStorage = ft.Text("")
    lunaUserProfileStatusStorage = ft.Text("")
    lunaStatus = ft.CupertinoTextField(placeholder_text="Update your status", on_submit=changeUserStatus, width=250)
    lunaErrorText = ft.Text("Please enter a username and password", color=ft.colors.WHITE)
    lunaSearch = ft.CupertinoTextField(placeholder_text="Search", color=messageTypeColor, bgcolor=dialogMessageBoxColor,
                                       placeholder_style=ft.TextStyle(size=15, color= messageTypeColor),
                                       on_submit=lunaSearchQuery)

    page.title = "lunaChat"
    page.bgcolor = pageBackgroundColor
    page.update()

    print(f"LOG receiving anonymous join on lunaChat instance "
          f"{settings.lunaChatName} ({settings.host}:{settings.port})")

    login = ft.CupertinoAlertDialog(
        open=True,
        modal=True,
        title=ft.Text("Welcome to lunaChat!", color=titleTextColor),
        content=ft.Column([lunaUsername, lunaPassword, lunaErrorText], tight=True),
        actions=[ft.CupertinoButton(text="Back", on_click=backToLoginHub, color=ft.colors.PINK,
                                    bgcolor=dialogButtonColor, padding=5),
                 ft.CupertinoButton(text="Login", on_click=joinClick, color=ft.colors.PINK,
                                    bgcolor=dialogButtonColor, padding=5)],
    )  # Opens the alert dialog welcoming the user to lunaChat and takes the input from the user which is the username

    register = ft.CupertinoAlertDialog(
        open=True,
        modal=True,
        title=ft.Text("Register an account on lunaChat!", color=titleTextColor),
        content=ft.Column([lunaUsername, lunaPassword, lunaErrorText], tight=True),
        actions=[ft.CupertinoButton(text="Back", on_click=backToLoginHub, color=ft.colors.PINK,
                                    bgcolor=dialogButtonColor, padding=5),
                 ft.CupertinoButton(text="Join lunaChat", on_click=createLunaChatAccount, color=ft.colors.PINK,
                                    bgcolor=dialogButtonColor, padding=5)],
    )

    menu = ft.CupertinoAlertDialog(
        open=True,
        modal=True,
        title=ft.Text("lunaChat Login Hub", color=titleTextColor),
        content=ft.Text(settings.lunaLoginMessage),
        actions=[ft.CupertinoButton(text="Login", on_click=loginMenu, color=ft.colors.PINK,
                                    bgcolor=dialogButtonColor, padding=5),
                 ft.CupertinoButton(text="Register", on_click=registerMenu, color=ft.colors.PINK,
                                    bgcolor=dialogButtonColor, padding=5)],
    )

    menuAccountRegisterDisabled = ft.CupertinoAlertDialog(
        open=True,
        modal=True,
        title=ft.Text("lunaChat Login Hub", color=titleTextColor),
        content=ft.Text(settings.lunaLoginMessage),
        actions=[ft.CupertinoButton(text="Login", on_click=loginMenu, color=ft.colors.PINK,
                                    bgcolor=dialogButtonColor, padding=5)],
    )

    accountCreated = ft.CupertinoAlertDialog(
        open=True,
        modal=True,
        title=ft.Text("Account Created Successfully", color=titleTextColor),
        actions=[ft.CupertinoButton(text="Back", on_click=backToLoginHub, color=ft.colors.PINK,
                                    bgcolor=dialogButtonColor, padding=5)],
    )

    deleteAccount = ft.CupertinoAlertDialog(
        open=True,
        modal=True,
        title=ft.Text("Delete Account", color=titleTextColor),
        content=ft.Column([lunaPassword, lunaErrorText], tight=True),
        actions=[ft.CupertinoButton(text="Back", color=ft.colors.PINK,
                                    bgcolor=dialogButtonColor, padding=5, on_click=closeDeleteAccountDialog),
                 ft.CupertinoButton(text="Delete Account", color=ft.colors.PINK,
                                    bgcolor=dialogButtonColor, padding=5, on_click=deleteLunaAccount)],
    )

    changePassword = ft.CupertinoAlertDialog(  # Add on_click functionality
        open=True,
        modal=True,
        title=ft.Text("Change Password", color=titleTextColor),
        content=ft.Column([lunaPassword, lunaChangePassword, lunaErrorText], tight=True),
        actions=[ft.CupertinoButton(text="Back", color=ft.colors.PINK,
                                    bgcolor=dialogButtonColor, padding=5, on_click=closeChangePasswordDialog),
                 ft.CupertinoButton(text="Save", color=ft.colors.PINK,
                                    bgcolor=dialogButtonColor, padding=5, on_click=changeUserPassword)],
    )

    def loginDialog():  # Display the login alert dialog
        """Open the Login dialog"""
        page.open(login)
        page.update()

    def deleteAccountDialog():
        """Open the Delete Account Dialog"""
        lunaErrorText.value = "Please enter your password"
        page.open(deleteAccount)
        page.update()

    def changePasswordDialog():
        """Open the Delete Account Dialog"""
        lunaErrorText.value = "Please enter your current password"
        page.open(changePassword)
        page.update()

    passwordDialog = ft.CupertinoAlertDialog(
        open=True,
        modal=True,
        title=ft.Text(f"Enter password for {settings.lunaChatName}'s lunaChat instance", color=titleTextColor),
        content=ft.Column([lunaServerPassword, lunaErrorText], tight=True),
        actions=[ft.CupertinoButton(text="Join", on_click=passwordCheck, color=ft.colors.PINK,
                                    bgcolor=dialogButtonColor, padding=5)],
    )

    def registerDialog():
        """Open the register dialog"""
        page.open(register)
        page.update()

    def displayLoginHub():
        """Open the Login Hub dialog"""
        page.open(menu)
        page.update()

    def displayLoginHubRegisterDisabled():
        """Open the Login Hub Register Disabled dialog"""
        page.open(menuAccountRegisterDisabled)
        page.update()

    def displayAccountCreated():
        """Open the Account Created Dialog"""
        page.open(accountCreated)
        page.update()

    def displayPasswordScreen():  # Display the password alert dialog
        """Open the Password Screen dialog"""
        page.open(passwordDialog)
        lunaErrorText.value = "Please enter the server password"
        lunaErrorText.update()
        page.update()

    if settings.serverPasswordRequired:  # If the server requires a password open up that dialog
        displayPasswordScreen()
    else:
        if settings.enableAccountCreation:
            page.go('/')
            displayLoginHub()
        else:
            displayLoginHubRegisterDisabled()

    # Close the description banner when the user clicks on the close button
    def closeDisplayDescription(e):
        """Close the lunaChat Instance description banner"""
        lunaChatDesc.open = False
        page.update()

    lunaChatDesc = ft.Banner(
        open=False,
        bgcolor=bannerBackgroundColor,
        leading=ft.Icon(ft.icons.DESCRIPTION, color=ft.colors.WHITE, size=40),
        content=ft.Text(settings.lunaDescription, color=bannerTextColor),
        actions=[ft.CupertinoButton("Close", on_click=closeDisplayDescription, color=bannerButtonTextColor,
                                    bgcolor=bannerButtonColor, padding=5)]

    )  # This is where all the contents of the description banner are defined

    # Display the description banner when the user clicks on the icon button
    def openDisplayDescription(e):
        """Open the lunaChat Instance description banner"""
        if lunaVersionInfo.open:
            lunaVersionInfo.open = False
        page.open(lunaChatDesc)
        page.update()

    # Close the version info banner when the user clicks on the close button
    def closeVersionInfo(e):
        """Close the lunaChat Version Info banner"""
        lunaVersionInfo.open = False
        page.update()

    lunaVersionInfo = ft.Banner(
        open=False,
        bgcolor=bannerBackgroundColor,
        leading=ft.Icon(ft.icons.INFO, color=ft.colors.WHITE, size=40),
        content=ft.Text(f"Version {currentVersion}", size=20, spans=[ft.TextSpan(
            f"{versionBranch}", ft.TextStyle(size=10, color=titleTextColor))], color=titleTextColor),
        actions=[ft.CupertinoButton("Close", on_click=closeVersionInfo, color=bannerButtonTextColor,
                                    bgcolor=bannerButtonColor, padding=5)]
    )  # This is where all the contents of the version info banner are defined

    # Display the version info banner when the user clicks on the icon button
    def openVersionInfo(e):
        """Open the lunaChat Version Info banner"""
        if lunaChatDesc:
            lunaChatDesc.open = False
        page.open(lunaVersionInfo)
        page.update()

    def addUsersToList():  # Add users to navigation drawer
        """Add users to the user list"""
        # This code needs to be restructured to support checking users activity in the DB
        username_count = 0
        with open('./config/usernamesInUse.txt') as readUsernames:  # Temporarily using usernamesInUse.txt for this
            usernamesInUse = readUsernames.readlines()  # Read all the usernames from the textfile into the list
            usernamesInUse = [line.rstrip('\n') for line in usernamesInUse]

        usernameList = []  # Where the navigation drawer destination for each user will be stored

        for username in usernamesInUse:
            conn = sqlite3.connect('lunaData.db')
            cursor = conn.cursor()

            # Grab the custom status message
            cursor.execute("SELECT customStatusMessage FROM accounts WHERE username = ?",
                           (username,))

            fetchUserStatus = cursor.fetchone()

            customStatusMessage = fetchUserStatus[0]

            if str(customStatusMessage) == "None":
                customStatusMessage = f"No status set by {username}"

            usernameList.append(ft.Row(controls=[
                ft.Icon(name=ft.icons.ACCOUNT_CIRCLE, color=chatMessageColor),
                ft.Text(f"{username} - \"{customStatusMessage}\" ")
            ]
            ))
            username_count = username_count + 1

        return usernameList, username_count

    def logOutLunaChat(e):
        """Logs the user out of the lunaChat instance"""
        page.go('/')
        with open('./config/usernamesInUse.txt') as readUsernames:  # Temporarily using usernamesInUse.txt for this
            usernamesInUse = readUsernames.readlines()  # Read all the usernames from the textfile into the list
            usernamesInUse = [line.rstrip('\n') for line in usernamesInUse]

        if lunaUserStorage.value.strip() in usernamesInUse:
            usernamesInUse.remove(f"{lunaUserStorage.value.strip()}")  # Free up the username from the list
            with open('./config/usernamesInUse.txt', "w") as writeUsernames:
                for username in usernamesInUse:
                    writeUsernames.write(username + "\n")

            if lunaUserStorage.value != "":
                page.pubsub.send_all_on_topic("Default", LunaMessage(lunaUser=lunaUserStorage.value,
                                                                     lunaText=f"{lunaUserStorage.value} has logged out of {settings.lunaChatName}'s "
                                                                              f"lunaChat instance",
                                                                     lunaMessageType="lunaLoginMessage", lunaKey=0))

                print(f"LOG (Message Type: lunaLoginMessage) {lunaUserStorage.value.strip()} has logged out of "
                      f"{settings.lunaChatName}'s lunaChat instance")

        if settings.serverPasswordRequired:  # If the server requires a password open up that dialog
            displayPasswordScreen()
        else:
            if settings.enableAccountCreation:
                displayLoginHub()
            else:
                displayLoginHubRegisterDisabled()

        lunaUsername.value = ""
        lunaPassword.value = ""

    def onDisconnect(e: ft.PageDisconnectedException):
        """Log out the user once they end the session"""
        try:
            logOutLunaChat("")
        except:
            print("User wasn't logged in")

    page.on_disconnect = onDisconnect

    def route_change(route):
        """For navigating between pages"""
        getUserList = addUsersToList()
        page.views.clear()
        page.views.append(
            ft.View(
                "/",
                [
                    ft.AppBar(
                        title=ft.Text(f"Login | lunaChat", size=20, weight=ft.FontWeight.BOLD,
                                      color=titleTextColor),
                        center_title=False,
                        bgcolor=pageBackgroundColor,
                        toolbar_height=40,
                    ),
                    ft.Container(
                        ft.Text(f"lunaChat {grabLunaInfo[0]}\nBuild {grabLunaInfo[3]}")
                    )
                ],
                bgcolor=pageBackgroundColor
            )
        )

        if page.route == f"/{settings.profilePortalName}":
            page.go(f'/{settings.profilePortalName}/{lunaUserStorage.value}')

        if page.route == f"/{settings.profilePortalName}/{lunaUserStorage.value}":
            if lunaUserStorage.value == "":
                page.go('/')
            else:
                page.views.append(
                    ft.View(
                        f"/{settings.profilePortalName}/{lunaUserStorage.value}",
                        [
                            ft.AppBar(
                                title=ft.Text(
                                    f"{lunaUserStorage.value}'s {settings.profilePortalDisplayName} | lunaChat",
                                    size=20,
                                    weight=ft.FontWeight.BOLD,
                                    color=titleTextColor),
                                automatically_imply_leading=False,
                                center_title=False,
                                bgcolor=pageBackgroundColor,
                                toolbar_height=40,
                                actions=[
                                    ft.IconButton(ft.icons.SEARCH, icon_color=ft.colors.PINK, on_click=lambda _:
                                    page.go("/search")),
                                    ft.IconButton(ft.icons.INFO, on_click=openVersionInfo, icon_color=ft.colors.PINK),
                                    ft.IconButton(ft.icons.DESCRIPTION, on_click=openDisplayDescription,
                                                  icon_color=ft.colors.PINK),
                                    ft.IconButton(ft.icons.LOGOUT, on_click=logOutLunaChat, icon_color=ft.colors.PINK),
                                    ft.IconButton(ft.icons.ACCOUNT_CIRCLE, icon_color=ft.colors.PINK,
                                                  on_click=lambda _: page.go(f"/{settings.chatPortalName}"))
                                ]),
                            ft.Container(
                                content=ft.Container(
                                    content=ft.Row(controls=[
                                        ft.Column(controls=[
                                            ft.Text("Profile Information"),
                                            ft.Row(controls=[
                                                ft.CircleAvatar(  # The avatar that will pop up in the message container
                                                    content=ft.Text(getInitials(lunaUserStorage.value)),
                                                    color=ft.colors.WHITE,
                                                    bgcolor=getAvatarColor(lunaUserStorage.value)),
                                                ft.Text(f"{lunaUserStorage.value}"),
                                            ]),
                                            ft.Text("            Online", color=ft.colors.BLUE),
                                            ft.Text(f"            Status: {lunaStatusStorage.value}"),
                                            lunaStatus,
                                            ft.Row(controls=[
                                                ft.CupertinoButton(text="Change Password", color=ft.colors.PINK,
                                                                   bgcolor=dialogButtonColor, padding=5,
                                                                   on_click=changePasswordMenu),
                                                ft.CupertinoButton(text="Delete Account", color=ft.colors.PINK,
                                                                   bgcolor=dialogButtonColor, padding=5,
                                                                   on_click=deleteAccountMenu)
                                            ]),

                                        ],
                                            expand=3,  # Set the ratio of how much width the column will take up
                                            alignment=ft.MainAxisAlignment.START,  # Set the alignment for this column
                                            height=300  # Set the height of the column
                                        ),
                                        ft.Column(controls=[
                                            ft.Text(f"Online - {getUserList[1]} Users Active", color=chatMessageColor),
                                            ft.Column(controls=[
                                                *getUserList[0],
                                            ], scroll=ft.ScrollMode.ADAPTIVE)
                                        ],
                                            expand=1,  # Set the ratio of how much width the column will take up
                                            alignment=ft.MainAxisAlignment.START,  # Set the alignment for this column
                                            height=300  # Set the height of the column
                                        )
                                    ], alignment=ft.MainAxisAlignment.START
                                    ), height=300
                                )
                            )
                        ],
                        bgcolor=pageBackgroundColor
                    )
                )

        if page.route == f"/profile/{lunaUserProfileStorage.value}":
            if lunaUserStorage.value == "":
                page.go('/')
            else:
                page.views.append(
                    ft.View(
                        f"/profile/{lunaUserProfileStorage.value}",
                        [
                            ft.AppBar(
                                title=ft.Text(f"{lunaUserProfileStorage.value}'s Profile | lunaChat", size=20,
                                              weight=ft.FontWeight.BOLD,
                                              color=titleTextColor),
                                automatically_imply_leading=False,
                                center_title=False,
                                bgcolor=pageBackgroundColor,
                                toolbar_height=40,
                                actions=[
                                    ft.IconButton(ft.icons.SEARCH, icon_color=ft.colors.PINK, on_click=lambda _:
                                    page.go("/search")),
                                    ft.IconButton(ft.icons.INFO, on_click=openVersionInfo, icon_color=ft.colors.PINK),
                                    ft.IconButton(ft.icons.DESCRIPTION, on_click=openDisplayDescription,
                                                  icon_color=ft.colors.PINK),
                                    ft.IconButton(ft.icons.LOGOUT, on_click=logOutLunaChat, icon_color=ft.colors.PINK),
                                    ft.IconButton(ft.icons.ACCOUNT_CIRCLE, icon_color=ft.colors.PINK,
                                                  on_click=lambda _: page.go("/chat"))
                                ]),
                            ft.Container(
                                content=ft.Container(
                                    content=ft.Row(controls=[
                                        ft.Column(controls=[
                                            ft.Text("Profile Information"),
                                            ft.Row(controls=[
                                                ft.CircleAvatar(  # The avatar that will pop up in the message container
                                                    content=ft.Text(getInitials(lunaUserProfileStorage.value)),
                                                    color=ft.colors.WHITE,
                                                    bgcolor=getAvatarColor(lunaUserProfileStorage.value)),
                                                ft.Text(f"{lunaUserProfileStorage.value}"),
                                            ]),
                                            ft.Text("            Activity Status Unknown", color=ft.colors.BLUE),
                                            ft.Text(f"            Status: {lunaUserProfileStatusStorage.value}"),

                                        ],
                                            expand=3,  # Set the ratio of how much width the column will take up
                                            alignment=ft.MainAxisAlignment.START,  # Set the alignment for this column
                                            height=300  # Set the height of the column
                                        ),
                                        ft.Column(controls=[
                                            ft.Text(f"Online - {getUserList[1]} Users Active", color=chatMessageColor),
                                            ft.Column(controls=[
                                                *getUserList[0],
                                            ], scroll=ft.ScrollMode.ADAPTIVE)
                                        ],
                                            expand=1,  # Set the ratio of how much width the column will take up
                                            alignment=ft.MainAxisAlignment.START,  # Set the alignment for this column
                                            height=300  # Set the height of the column
                                        )
                                    ], alignment=ft.MainAxisAlignment.START
                                    ), height=300
                                )
                            )
                        ],
                        bgcolor=pageBackgroundColor
                    )
                )

        if page.route == f"/{settings.chatPortalName}":
            if lunaUserStorage.value == "":
                page.go('/')
            else:
                page.views.append(
                    ft.View(
                        f"/{settings.chatPortalName}",
                        [
                            ft.AppBar(
                                title=ft.Text(f"{settings.lunaChatName} | lunaChat", size=20, weight=ft.FontWeight.BOLD,
                                              color=titleTextColor),
                                center_title=False,
                                bgcolor=pageBackgroundColor,
                                toolbar_height=40,
                                actions=[
                                    ft.IconButton(ft.icons.SEARCH, icon_color=ft.colors.PINK, on_click=lambda _:
                                    page.go("/search")),
                                    ft.IconButton(ft.icons.INFO, on_click=openVersionInfo, icon_color=ft.colors.PINK),
                                    ft.IconButton(ft.icons.DESCRIPTION, on_click=openDisplayDescription,
                                                  icon_color=ft.colors.PINK),
                                    ft.IconButton(ft.icons.LOGOUT, on_click=logOutLunaChat, icon_color=ft.colors.PINK),
                                    ft.IconButton(ft.icons.ACCOUNT_CIRCLE, icon_color=ft.colors.PINK,
                                                  on_click=lambda _: page.go(
                                                      f"/{settings.profilePortalName}/{lunaUserStorage.value}"))
                                ],
                                automatically_imply_leading=False
                            ),
                            lunaChat,
                            ft.Row(controls=[newMessage,
                                             ft.IconButton(
                                                 icon=ft.icons.SEND_ROUNDED,
                                                 bgcolor=ft.colors.PINK_100,
                                                 icon_color=ft.colors.PINK,
                                                 icon_size=20,
                                                 on_click=sendClick
                                             )])

                        ],
                        bgcolor=pageBackgroundColor,

                    )
                )

        if page.route == f"/search":
            if lunaUserStorage.value == "":
                page.go('/')
            else:
                page.views.append(
                    ft.View(
                        f"/search",
                        [
                            ft.AppBar(
                                title=ft.Text(f"Search | lunaChat", size=20,
                                                weight=ft.FontWeight.BOLD,
                                                color=titleTextColor),
                                automatically_imply_leading=False,
                                center_title=False,
                                bgcolor=pageBackgroundColor,
                                toolbar_height=40,
                                actions=[
                                    ft.IconButton(ft.icons.SEARCH, icon_color=ft.colors.PINK, on_click=lambda _:
                                    page.go("/chat")),
                                    ft.IconButton(ft.icons.INFO, on_click=openVersionInfo,
                                                    icon_color=ft.colors.PINK),
                                    ft.IconButton(ft.icons.DESCRIPTION, on_click=openDisplayDescription,
                                                    icon_color=ft.colors.PINK),
                                    ft.IconButton(ft.icons.LOGOUT, on_click=logOutLunaChat,
                                                    icon_color=ft.colors.PINK),
                                    ft.IconButton(ft.icons.ACCOUNT_CIRCLE, icon_color=ft.colors.PINK,
                                                    on_click=lambda _: page.go("/profile"))
                                ]),
                            ft.Container(
                                content=ft.Container(
                                    content=ft.Column(controls=[
                                        ft.Text("Search"),
                                        lunaSearch

                                    ],
                                        alignment=ft.MainAxisAlignment.CENTER,
                                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                        width=500
                                    ), alignment=ft.alignment.center


                                )
                            )

                        ],
                        bgcolor=pageBackgroundColor,

                    )
                )
        page.update()

    def page_pop(view):  # Go back to previous page
        page.views.pop()
        top_view = page.views[0]
        page.go(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = page_pop
    page.go(page.route)


ft.app(main, assets_dir="assets", view=ft.AppView.WEB_BROWSER, host=settings.host, port=settings.port)
