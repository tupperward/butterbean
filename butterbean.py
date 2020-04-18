#Butterbean DiscordBot for WATTBA Discord 
#author: Tupperward
#content contributors: Smoltz, Jackapedia

#Thank you to Agnes(Smyrna) for providing guidance throughout the whole process

#Importing dependencies
import discord; import os; import random; import psycopg2; import asyncio
from bobross import embedRossIcon
from bobross import rossQuotes
from discord.ext import commands, tasks
from discord.utils import get
from config import config
import bovonto

#Intializing functions
client = commands.Bot(command_prefix='!', description='Butterborg is online.', add=True)
#Intializing ready    
@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('-------')
    print('Resistance is futile.')

#DATABASE_URL = os.environ['DATABASE_URL']

params = config()
conn = psycopg2.connect(**params)
cur = conn.cursor()

greetMessage = "Welcome to the WATTBA-sistance! Please take your time to observe our rules and, if you're comfortable, use the **!callme** command to tag yourself with your pronouns. Available pronouns are **!callme he/him**, **!callme she/her**, **!callme they/them**, **!callme xe/xem** and **!callme ze/zir** If you get tired of your pronouns you can remove them with **!imnot** \n\n There are several other roles you can **!join** too, like **!join streampiggies** to be notified of Eli's streams. Check them out by using **!listroles**. \n\n Oh, and feel free to get an inspirational Bob Ross quote any time with **!bobross**. \n\n This server also uses this bot for meme purposes. Be on the lookout for memes you can send using by sending **!bb** and the name of the meme. You can find a list of those memes with **!beanfo**"
timeyIcon = 'https://i.imgur.com/vtkIVnl.png'
unapprovedDeny = "Uh uh uh! {0} didn't say the magic word!\nhttps://imgur.com/IiaYjzH.gif"

def listToString(s):
    str1 = " "
    return (str1.join(s).replace(" ", ", "))

async def checkApprovedUsers(user):
    lookupString = "SELECT username FROM approved_users WHERE username LIKE  '%{}%';".format(user)
    cur.execute(lookupString)
    check = cur.fetchone()
    if not check is None:
        return True

# ---------------- Meme Management ----------------
#Message Send with !bb arg
@client.command()
async def bb(ctx, arg):
    params = config()
    conn = psycopg2.connect(**params)
    cur = conn.cursor()

    search = arg.lower()
    lookupString = "SELECT link FROM posts WHERE post_name LIKE '%{}%';".format(search)
    cur.execute(lookupString)
    response = cur.fetchone()
    conn.close()
    if response is None:
        await ctx.send("Sorry, this command doesn't exist.")
    else:
        split = response[0].replace("'",'')
        await ctx.send(split)

#Mods can add items to the list
@client.command()
async def add(ctx, key, val):
    params = config()
    conn = psycopg2.connect(**params)
    cur = conn.cursor()
    key = key.lower()

    if await checkApprovedUsers(ctx.message.author):
        lookupString = "INSERT INTO posts VALUES ('{0}','{1}');".format(key,val)
        cur.execute(lookupString)
        conn.commit()
        conn.close()
        await ctx.send("{} has been added to my necroborgic memories".format(key))
    else:
        await ctx.send(unapprovedDeny.format(ctx.message.author))

#Mods can remove items from the list
@client.command()
async def remove (ctx, key): 
    params = config()
    conn = psycopg2.connect(**params)
    cur = conn.cursor()
    key = key.lower()

    if await checkApprovedUsers(ctx.message.author):

        lookupString = "DELETE FROM posts WHERE post_name LIKE '%{}%';".format(key)
        cur.execute(lookupString)
        conn.commit()
        conn.close()
        await ctx.send("{} has been purged from my necroborgic memories".format(key))
    else:
        await ctx.send(unapprovedDeny.format(ctx.message.author))

#Lists all meme commands
@client.command()
async def beanfo(ctx):
    #embed = discord.Embed(title='List of commands', color=0xeee657)
    params = config()
    conn = psycopg2.connect(**params)
    cur = conn.cursor()
    
    cur.execute('SELECT post_name FROM posts;')
    info = cur.fetchall()
    finalList = []
    for i in info:
        finalList.append(i[0].replace("'",''))

    conn.close()
    await ctx.send(listToString(finalList))
    

# ---------------- New Member Welcome ----------------
#Welcomes a new member
@client.event
async def on_member_join( member):
    guild = member.guild
    if guild.system_channel is not None:
        eMessage = discord.Embed(description="{0.mention}! {1}".format(member, greetMessage))
        eMessage.set_author(name='Timey', icon_url=timeyIcon)
        await guild.system_channel.send(embed=eMessage)

#If needed, will resend the welcome message
@client.command()
async def resend(ctx):
    eMessage = discord.Embed(description="{0}".format(greetMessage))
    eMessage.set_author(name='Timey', icon_url=timeyIcon)
    await ctx.send(embed=eMessage)

#Bob Ross quote
@client.command()
async def bobross (ctx):
# Posts quotes of Bob Ross
    rand_c = random.randint(0, len(rossQuotes) - 1)
    quote = rossQuotes[rand_c]
    e = discord.Embed(description=quote)
    e.set_author(name="Bob Ross", icon_url=embedRossIcon)
    await ctx.send(embed=e)

async def makePitch():
    await client.wait_until_ready()
    channelChoices = [465938202503413771,465991265557676054,644678362413006909,465950091044454411,466672962506981406]
    print('Step one')

    while client.is_ready:
        cycleChannels = random.randrange(len(channelChoices))
        print(cycleChannels)
        targetChannel = channelChoices[cycleChannels]
        print('Step two')
        setChannel = client.get_channel(targetChannel)
        print(targetChannel)
        rand_c = random.randint(0, len(bovonto.pitches) -1)
        pitch = bovonto.pitches[rand_c]
        e = discord.Embed(description=pitch)
        e.set_author(name="Bovonto Bot", icon_url=bovonto.embedBovontoIcon)
        await setChannel.send(embed=e)
        await asyncio.sleep(random.randrange(360,43200))

#---------------- Role management functions ----------------
#Adds a pronoun specific role
@client.command()
async def callme (ctx, genderName):
    user = ctx.message.author
    genderId = discord.utils.get(ctx.guild.roles, name=genderName)
    upperDemarc = discord.utils.get(ctx.guild.roles, name='he/him'); lowerDemarc = discord.utils.get(ctx.guild.roles, name='Catillac Cat')
    if genderId > upperDemarc or genderId <= lowerDemarc:
        await ctx.send('<:rudy:441453959215972352> Oooooh, {0} isn\'t as sneaky as they think they are. '.format(user.mention))
    elif genderId <= upperDemarc and genderId > lowerDemarc:
        userRoles = ctx.author.roles
        if genderId in userRoles:
            await ctx.send('<:rudy:441453959215972352> You already have {0} pronouns.'.format(genderName))
        if genderId not in userRoles:
            await user.add_roles(genderId)
            await ctx.send('<:heathsalute:482273509951799296> Comrade {0} wants to be called {1}.'.format(user.mention, genderName))

#Removes a pronoun specific role          
@client.command()
async def imnot(ctx, oldRole):
    user = ctx.message.author
    roleToRemove = discord.utils.get(ctx.guild.roles, name=oldRole)
    userRoles = ctx.author.roles
    await user.remove_roles(roleToRemove)
    await ctx.send('<:heathsalute:482273509951799296> Comrade {0} no longer wants to be called {1}.'.format(user.mention, oldRole))
    if roleToRemove not in userRoles:
        await ctx.send("<:rudy:441453959215972352> You never picked those pronouns.")

#Adds a non-pronoun specific role
@client.command()
async def join(ctx, newRole):
    user = ctx.message.author
    roleToAdd = discord.utils.get(ctx.guild.roles, name=newRole.lower())
    lowerDemarc = discord.utils.get(ctx.guild.roles, name='Catillac Cat')
    if roleToAdd >= lowerDemarc:
        await ctx.send("<:rudy:441453959215972352> That's not what this is for.")
    else:
        await user.add_roles(roleToAdd)
        await ctx.send('<:heathsalute:482273509951799296> {0} has joined {1}!'.format(user.mention, newRole))

#Removes a non-pronoun specific role
@client.command()
async def leave(ctx, oldRole):
    user = ctx.message.author
    roleToRemove = discord.utils.get(ctx.guild.roles, name=oldRole.lower())
    userRoles = ctx.author.roles
    await user.remove_roles(roleToRemove)
    await ctx.send('{0} is no longer a member of {1}.'.format(user.mention, oldRole))
    if roleToRemove not in userRoles:
        await ctx.send("<:rudy:441453959215972352> You were never in that role.")

#Lists unformatted all roles.  
@client.command()
async def listroles(ctx):
    rolesStr = ''
    roles = ctx.guild.roles
    for i in roles:
        rolesStr += " " + str(i) +","
    await ctx.send(rolesStr)

client.loop.create_task(makePitch())

#Actually running the damn thing
client.run(os.environ['BOT_TOKEN'])