# WATTBA-Butterbean
A bot for the WATTBA discord

__Prereqs__:
- docker 
- docker-compose or docker compose
- set message_contents to True in Intents panel on the app page.

This is some dumb bullshit I've hacked together without any research for the past like 3-4 years now. It's not good. Do not use this as an example of a quality discord bot in python. The main bot here is wildly out of date and likely not going to see too many new features. Jinx brought it into line with Intents but there's a lot more work to make this a "modern" chatbot.

As it stands with this version, it can be self hosted. You can load your backup of the .db by placing it in `/app/config/`. It must be named `butterbean.db`.

There a `.env` in `/app/config` that you will have to complete as well. Just provide the discord bot token in the `TOKEN` environment variable.

Once you've modified your `.env` file, running `docker compose up -d` or `docker-compose up -d` will get you started.

A new image of this container is available every Monday at midnight. `0 0 * * 1` 