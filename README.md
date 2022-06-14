# WATTBA-Butterbean
A bot for the WATTBA discord

__Prereqs__:
- docker compose (so like docker engine 20+ I think)

This is some dumb bullshit I've hacked together without any research for the past like 3-4 years now. It's not good. Do not use this as an example of a quality discord bot in python. The main bot here is wildly out of date and likely not going to see too many new features.

As it stands with this version, it can be self hosted. If you have a backup butterbean.sql just load it into `db/butterbean.sql` and get running.

There a `.env` that you will have to complete as well. It's pretty self explanatory, the only thing you ened to add is your Bot's OAuth token.

Otherwise, `make build && make start` should bring the bot up to speed.
