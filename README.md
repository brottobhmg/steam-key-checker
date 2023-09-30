# Usage
Insert into TELEGRAM_TOKEN your Bot token

Insert into TELEGRAM_CHATID your Telegram chatid

Insert into STEAM_USERNAME your username on Steam

Insert into STEAM_PASSWORD your password on Steam

Run the .py file.
If you don't have Python environment, download and run the .exe in the [releases tab](https://github.com/brottobhmg/steam-key-checker/releases)

# TL;DR
Generate ==> Check ==(positive)==> Notify

# What is this?
This script allow you to create a random product key for [Steam](https://store.steampowered.com/), check if is valid and, in positive case, notify it to your bot on Telegram and print it on screen.

To create the API request, it need to access to your Steam account to retrieve the sessionID.

It can check 10 keys every 60 minuts. Yes, isn't fast. If you know how to speed up open an issue.



# How many games can i find ?
You have to be very very very lucky to find one.

The product key is composed by three series of five numbers - example A1B2C-3D4E5-F6G7H - and every position can be letter [A,Z] or number [0,9].

So, 35^15 possible combinations
🤯

# Why don't generate a list of all possible combinations and check it?
All combinations like this AAAA-AAAAA-XXXXX saved in .txt file, weigh 1GB.

So too much GB (or TB) to store.


