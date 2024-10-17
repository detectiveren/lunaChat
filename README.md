# lunaChat
[![Python application](https://github.com/detectiveren/lunaChat/actions/workflows/python-app.yml/badge.svg)](https://github.com/detectiveren/lunaChat/actions/workflows/python-app.yml)
[![Static Badge](https://img.shields.io/badge/v1.0.0%20alpha2-Documentation?style=flat&logo=GitHub&logoColor=white&label=Get&labelColor=black&color=blue)](https://github.com/detectiveren/lunaChat/releases)



lunaChat is an app that is built on Python and Flet (powered by Flutter), currently it is a chat app that can send and recieve messages across a lunaChat instance. This application is currently in development and advanced features will be introduced later on.

## Screenshots

- Light Mode
![image](https://github.com/user-attachments/assets/62786fbb-cb64-4da6-be1d-f504ee749b85)


- Dark Mode
![image](https://github.com/user-attachments/assets/1771c3ac-e4d1-4acc-b185-cd9e67261394)




## How to host your own lunaChat

- Install Python 3.12
- Install the dependancies ```pip install -r requirements.txt```
- Ensure you are in the root directory of the source code folder you extracted
- Modify settings.py to your liking, for example you can change the host and port
- Go into your terminal and cd into the source code directory
- To run the application, type ```python3 luna.py```
- Enjoy!

## What can you currently do in lunaChat?

- Set up your own lunaChat instance, change the host and port if you want to make it public or work across LAN ```check settings.py```
- Set up a name for your own lunaChat instance ```check settings.py```
- Set up a description for your lunaChat instance ```check settings.py```
- Set a password for your lunaChat instance ```check settings.py```
- Create an account on lunaChat
- Login to the account you created on lunaChat
- Set a custom status
- Send and receive text messages in a lunaChat instance
- Send and receive embedded images and GIFs
- Ban specific usernames using a banned usernames list ```check config/bannedUsernames.txt```
- Ban specific words using a banned words list ```check config/bannedWords.txt```
- Interact with lunaBOT

## What are the planned features for lunaChat?

- Encryption (so that messages are protected)
- Sending and receiving images and videos
- Further commands to interact with lunaBOT more
- Further customization of lunaChat
- Setting profile pictures
- Channel based system
- and more!

## Interacting with lunaBOT

So far lunaBOT is still really early and can only do a couple of commands, further upgrades are planned for lunaBOT so look out for that.

- ```!lunaBOT buildNumber``` will make lunaBOT print the build number
- ```!lunaBOT commands``` will make lunaBOT display a full list of commands
