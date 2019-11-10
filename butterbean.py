#Butterbean DiscordBot for WATTBA Discord 
#author: Tupperward
#content contributors: Smoltz, Jackapedia

#Thank you to Agnes(Smyrna) for providing guidance throughout the whole process

#Importing dependencies
import discord; import os; import random; import psycopg2
from bobross import embedRossIcon
from bobross import rossQuotes
from discord.ext import commands
from discord.utils import get
from config import config, sanitize

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

greetMessage = "Welcome to the WATTBA-sistance! Please take your time to observe our rules and, if you're comfortable, use the **!callme** command to tag yourself with your pronouns. Available pronouns are **he/him**, **she/her**, **they/them**, **xe/xem** and **ze/zir** If you get tired of your pronouns you can remove them with **!imnot** \n\n There are several other roles you can **!join** too, like **Streampiggies** to be notified of Eli's streams. Check them out by using **!listroles**. \n\n Oh, and feel free to get an inspirational Bob Ross quote any time with **!bobross**. \n\n This server also uses this bot for meme purposes. Be on the lookout for memes you can send using by sending **!bb** and the name of the meme."

unapprovedDeny = "Uh uh uh! {0} didn't say the magic word!\nhttps://imgur.com/IiaYjzH"

def convertTuple(tup):
    stringFormat = ''.join(tup)
    return stringFormat

async def checkApprovedUsers(user):
    await cur.execute("SELECT * FROM approved_users;")
    check = cur.fetchall()
    results = []
    for entry in check:
        formatted = convertTuple(entry)
        results.append(formatted)
    if user in results:
        return True
    else:
        return False

# ---------------- Meme Management ----------------
#Message Send with !bb arg
@client.command()
async def bb(ctx, arg):
    print (ctx.message.content)
    await cur.execute("SELECT link FROM posts WHERE post_name LIKE '%s';"%  ctx.message.content)
    response = cur.fetchone()
    message = response[0]
    
    await ctx.send(message)

#Mods can add items to the list
@client.command()
async def add(ctx, key, val):
    if checkApprovedUsers(ctx.message.author):
        await cur.execute("INSERT INTO posts VALUES ('{0}','{1}');".format(key,val))
        await conn.commit()
        await ctx.send("%s has been added to my necroborgic memories" % (key))
    else:
        await ctx.send(unapprovedDeny.format(ctx.message.author))

#Mods can remove items from the list
@client.command()
async def remove (ctx, key): 
    if checkApprovedUsers(ctx.message.author):
        await cur.execute("DELETE FROM posts WHERE post_name LIKE '%s';"% (key))
        await conn.commit()
        await ctx.send("%s has been purged from my necroborgic memories" % (key))
    else:
        await ctx.send(unapprovedDeny.format(ctx.message.author))

#Lists all meme commands
@client.command()
async def beanfo(ctx):
    #embed = discord.Embed(title='List of commands', color=0xeee657)
    beanfoDict = {}
    await cur.execute('SELECT * FROM posts;')
    beanfoDict.update(cur.fetchall())
    await ctx.send(beanfoDict)

# ---------------- New Member Welcome ----------------
#Welcomes a new member
@client.event
async def on_member_join( member):
    guild = member.guild
    if guild.system_channel is not None:
        eMessage = discord.Embed(description="{0.mention}! {1}".format(member, greetMessage))
        await guild.system_channel.send(embed=eMessage)

#If needed, will resend the welcome message
@client.command()
async def resend(ctx):
    eMessage = discord.Embed(description="{0}".format(greetMessage))
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

#Actually running the damn thing
client.run(os.environ['BOT_TOKEN'])