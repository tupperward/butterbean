
import random
import discord
import asyncio

def pickRandomLine(name, icon, lines):
    randLine = random.randint(0, len(lines) - 1)
    line = lines[randLine]
    e = discord.Embed(description=line)
    e.set_author(name=name, icon_url=icon)
    return e

async def makePitch(client):
    #Sets up status as ready
    await client.wait_until_ready()
    #Defines channels to send to (TOKENIZE THIS ASAP)
    channelChoices = [465938202503413771,465991265557676054,644678362413006909,465950091044454411,466672962506981406]

    #Loops through and chooses channels to send pitch to
    while client.is_ready:
        cycleChannels = random.randrange(len(channelChoices))
        targetChannel = channelChoices[cycleChannels]
        setChannel = client.get_channel(targetChannel)
        await setChannel.send(embed=pickRandomLine(name='Bovonto Bot', icon= embedBovontoIcon, lines=pitches))
        await asyncio.sleep(random.randrange(360,14400))

embedBovontoIcon = "https://imgur.com/8aCQlV5.png"
pitches = [
"Hello, weary traveller! May I slake your thirst with a frosty Bovonto?",
"Ah! In this summer heat a Bovonto will keep you cool!",
"Good poster! May I interest you in a Bovonto this day?",
"The pleasure of a Bovonto is nontrivial! Please, enjoy!",
"To delight in a Bovonto: a simple, gracious treat!",
"It is much like a dip in the ocean, to sup the Bovonto liquid!",
"At this time of day we all feel down. Why not a crisp Bovonto to life your spirits?",
"As the seasons change, so do our desires. Only the craving of Bovonto is perennial!",
"Find in your heart the thirst for Bovonto!",
"Bovonto: a wet treat!",
"Tears of joy from an angel drizzle off a cloud and land precisely in a sleek bottle. Bovonto is born!",
"What a performance! Bravo, Bovonto!",
"It is impossible to frown while swallowing Bovonto!",
"The world is full of uncountable sorrows. Bovonto may not cure them all, but it cannot hurt to try!",
"Gold is not always gold. Sometimes it is the deep purple hue of Bovonto!",
"The 'Dastardly Case of the Mondays' can be solved by Detective Bovonto! Please, try one!",
"To drink a Bovonto: A blessing of Christ!",
"For every liter of blood in your body, I recommend an ounce of delicious Bovonto!",
"If Bovonto were currency, all seekers of refreshment would be rich!",
"Please, do not shy away from your feelings. Find in Bovonto the strength to speak out!",
"I am a machine! To spread Bovonto's gospel, my purpose! Would you indulge me?",
"Soldiers die. Forests burn. Bovonto Refreshes!",
"Bovonto has been tied to fewer urinary tract infections than any other grape cola. Please enjoy!",
"Weep not for the lost. Drink Bovonto in their name!",
"Leap for joy, bliss is here! Bovonto!",
"Drink deep from the bottle, and your deepest wish will be granted: Bovonto.",
"The rock of plenty, the rock of faith: Bovonto"
]