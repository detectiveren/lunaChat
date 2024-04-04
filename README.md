# lunaChat
[![Python application](https://github.com/detectiveren/lunaChat/actions/workflows/python-app.yml/badge.svg)](https://github.com/detectiveren/lunaChat/actions/workflows/python-app.yml)
[![Static Badge](https://img.shields.io/badge/v1.0.0%20alpha1-Documentation?style=flat&logo=GitHub&logoColor=white&label=Get&labelColor=black&color=blue)](https://github.com/detectiveren/lunaChat/releases)



lunaChat is an app that is built on Python and Flutter, currently it is a chat app that can send and recieve messages across a lunaChat instance. This application is currently in development and advanced features will be introduced later on.

## Screenshots

- lunaChat Style
![image](https://github.com/detectiveren/lunaChat/assets/55319774/b709a751-0627-465f-8025-6492255d4b68)
- Dark Mode
![image](https://github.com/detectiveren/lunaChat/assets/55319774/21e9ba89-878b-4c88-bda5-b54b267e0788)



## How to host your own lunaChat

- Install Python 3.12
- Install the dependancies ```pip install -r requirements.txt```
- Ensure you are in the root directory of the source code folder you extracted
- Modify settings.py to your liking, at the moment you can only change the host and port
- Go into your terminal and cd into the source code directory
- To run the application, type ```python3 luna.py```
- Enjoy!

## What can you currently do in lunaChat?

- Set up your own lunaChat instance, change the host and port if you want to make it public or work across LAN ```check settings.py```
- Set up a name for your own lunaChat instance ```check settings.py```
- Set up a description for your lunaChat instance ```check settings.py```
- Set a password for your lunaChat instance ```check settings.py```
- Enter a username when you login to a lunaChat instance
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

So far lunaBOT is still really early and can only do one command which is telling you what the build number is, further upgrades are planned for lunaBOT so look out for that.

- ```!lunaBOT buildNumber``` will make lunaBOT print the build number
- ```!lunaBOT commands``` will make lunaBOT display a full list of commands
