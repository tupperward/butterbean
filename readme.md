# WATTBA-Butterbean
A bot for the WATTBA discord

__Prereqs__:
- docker 
- docker-compose or docker compose
- set message_contents to True in Intents panel on the app page.

This is some dumb bullshit I've hacked together without any research for the past like 3-4 years now. It's not good. Do not use this as an example of a quality discord bot in python. The main bot here is wildly out of date and likely not going to see too many new features. I brought it into line with Intents but there's a lot more work to make this a "modern" chatbot. I might return to it one day, but for now I'm going to put it to rest.

As it stands with this version, it can be self hosted. If you have a backup butterbean.sql just load it into `db/foo.sql` and get running.

There a `.env` that you will have to complete as well. It's pretty self explanatory, the only thing you ened to add is your Bot's token. Right now, do not change any other variables there. I need to do a little bit of configuration for the restore script to get that to work. Or just remove it entirely but I hate publishing static values. If you have suggestions let me know.

Simply running `docker compose up -d` or `docker-compose up -d` will get you started.