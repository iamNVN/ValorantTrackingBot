# Valorant Tracking Bot (Discord)

Hello! This is a Discord companion that lets users **monitor their favorite players** effortlessly.
Just add a player to your watchlist, and our bot will keep you posted on their matches. Get notified with essential stats like wins, kills, deaths, assists, and even the map and mode.

![Screenshot](https://github.com/iamNVN/ValorantTrackingBot/blob/main/images/Screenshot%202024-05-01%20153142.png?raw=true)


## Commands
- ```/watchadd name#tag``` - Add a player to watchlist
- ```/watchremove name#tag``` - Remove a player from watchlist
- ```/watchlist``` - View players being tracked in a channel

## Installation

1. Download the [project file](https://github.com/iamNVN/ValorantTrackingBot/archive/refs/heads/main.zip)
2. In the project root directory, run the following code to install dependencies: 
    ```bash
     pip install requirements.txt
     ```
3. Modify variables in ```.env-config``` and then rename the file to ```.env```
4. In the project root directory, run the following code to run the bot: 

    ```bash
     python bot.py
     ```


## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

Please make sure to update tests as appropriate.
