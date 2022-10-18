#Butterbean DiscordBot for WATTBA Discord 
#author: Tupperward

#Importing dependencies
from importlib.metadata import MetadataPathFinder
import discord, os , random, asyncio
from discord.ext import commands, tasks
from discord.utils import get

from modules.tarot_data import tarotData
from modules.permissions import checkPerms, addPerms, removePerms

from sqlalchemy import create_engine, table, text, Table, Column, CheckConstraint, DefaultClause, String, Integer, MetaData, select, insert
from sqlalchemy.orm import Session


#-----------Buttons!-----------#
bovontoSchedule = False

#-----------Get privileged intents so we can be in compliance with the API  -----------#
intents = discord.Intents.default()
intents.messages = True
intents.members = True
intents.message_content = True  

#-----------Intializing functions-----------#
client = commands.Bot(command_prefix=('!'), description='Butterborg is online.', add=True, intents=intents)

#-----------Intializing ready-----------#   
@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('-------')
    print('Resistance is futile.')
    print('Syncing command tree...')
    known_commands = await client.tree.sync()
    print('Command tree synced. {0} commands in tree.'.format(len(known_commands)))


greetMessage = "Welcome to the WATTBA-sistance! Please take your time to observe our rules and, if you're comfortable, use the **!callme** command to tag yourself with your pronouns. Available pronouns are **!callme he/him**, **!callme she/her**, **!callme they/them**, as well as several neopronouns. If you want to change your pronouns you can remove them with **!imnot** \n\nThere are several other roles you can **!join** too, like **!join streampiggies** to be notified of Eli's streams. Check them out by using **!listroles**. \n\nFeel free to reach out to any of our mods for any reason, they're always happy to talk: Criss (aka Criss or @Carissa) or Hugo (aka Furby or @hugs). \n\nThis server also uses this bot for meme purposes. Be on the lookout for memes you can send using by sending **!bb** and the name of the meme. You can find a list of those memes with **!beanfo**"
timeyIcon = 'https://i.imgur.com/vtkIVnl.png'
unapprovedDeny = "Uh uh uh! {0} didn't say the magic word!\nhttps://imgur.com/IiaYjzH.gif"


#---------------- Database Init ----------------
#Starts the db engine with sqlalchemy.
engine = create_engine("sqlite+pysqlite:///db/butterbean.db", echo=True, future=True)

#---------------- Helper functions ----------------
# Cleans special characters off of a string. Returns string without any special charactes
#* Returns String
#! Can be dangerous if used on URI
async def cleanString(res: str) -> str:
    specialChars = "!$%^&*()',"
    for char in specialChars:
        res = res.replace(char,'')
    return str(res)

# Checks to determine if user is approved to add/remove to Butterbean. 
#* Returns Boolean
# TODO #23 Change this to checking for a `deputy` level role instead of using the database. 
async def checkApprovedUsers(user: str) -> bool:
    lookupString = "SELECT COUNT(1) FROM approved_users WHERE username LIKE  '%{}%';".format(user)
    with Session(engine) as session:
        session.begin()
        try:
            response = session.execute(text(lookupString)).fetchone()
        except:
            print('Failed to query approved_users')
        check = await cleanString(str(response[0]))
        return int(check)

async def pickRandomRow(tableName: str, columnName: str) -> str:
    with Session(engine) as session:
        allRows = "SELECT COUNT(*) FROM {}".format(tableName)
        totalRows = session.execute(allRows).fetchone()
        randomLine = random.randint(1,totalRows)
        statement = "SELECT {} FROM {} WHERE id={};".format(columnName, tableName, randomLine)
        result = session.execute(statement).fetchone()
    return result[0]

async def createEmbedFromRandomLine(name: str, icon: str, tableName: str, columnName: str) -> str:
    line = await pickRandomRow(tableName, columnName)
    e = discord.Embed(description=line)
    e.set_author(name=name, icon_url=icon)
    return e

# ---------------- Meme Management ----------------
#Message Send with !bb arg
@client.hybrid_command(brief='Send a meme', description='Retrieves a stored meme from my necroborgic memories')
async def bb(ctx, meme: str):
    with Session(engine) as session:
        session.begin()        
        search = meme.lower()
        lookupString = "SELECT link FROM posts WHERE post_name LIKE '%{}%';".format(search)
        try:
            response = session.execute(text(lookupString)).fetchone()
        except:
            print('Failed to query posts for {}'.format(search))
        
        if response is None:
            await ctx.send("Sorry, this command doesn't exist.")
        else:
            link = await cleanString(str(response[0]))
            await ctx.send(link)

#Mods can add items to the list
@client.hybrid_command(brief='Add a meme', description='Adds a meme to my necroborgic memories, if you have permission')
async def add(ctx, name: str, url: str):
    if await checkApprovedUsers(ctx.message.author):
        with Session(engine) as session:
            session.begin()
            lookupString = "INSERT INTO posts (post_name, link) VALUES ('{0}','{1}');".format(name, url)
            session.execute(text(lookupString))
            session.commit()
            await ctx.send("{} has been added to my necroborgic memories".format(name))
    else:
        await ctx.send(unapprovedDeny.format(ctx.message.author))

@client.hybrid_command(brief='Add a trusted user', description='Gives a user permission to add/remove to Butterbean')
async def adduser(ctx, name: str):
    if await checkApprovedUsers(ctx.message.author):
        with Session(engine) as session:
            session.begin()
            lookupString = "INSERT INTO approved_users(username)"

#Mods can remove items from the list
@client.hybrid_command(brief='Remove a meme', description='Removes a meme from my necroborgic memories, if you have permission')
async def remove (ctx, meme: str): 
    if await checkApprovedUsers(ctx.message.author):
        with Session(engine) as session:
            session.begin()
            lookupString = "DELETE FROM posts WHERE post_name LIKE '%{}%';".format(meme)
            session.execute(text(lookupString))
            session.commit()
            await ctx.send("{} has been purged from my necroborgic memories".format(meme))
    else:
        await ctx.send(unapprovedDeny.format(ctx.message.author))

#Lists all meme commands
@client.hybrid_command(brief='List all memes', description='Lists all memes stored in my necroborgic memories')
async def beanfo(ctx):
    #Cleans up returned values from databases
    def listToString(s):
        str1 = " "
        return (str1.join(s).replace(" ", ", "))

    with Session(engine) as session:
        session.begin()
        info = session.execute(text('SELECT post_name FROM posts;'))
        
        finalList = []
        for i in info:
            finalList.append(i[0].replace("'",''))

        await ctx.send(listToString(finalList))


# ---------------- New Member Welcome ----------------
#Welcomes a new member
@client.event
async def on_member_join(member):
    guild = member.guild
    if guild.system_channel is not None:
        eMessage = discord.Embed(description="{0.mention}! {1}".format(member, greetMessage))
        eMessage.set_author(name='Timey', icon_url=timeyIcon)
        await guild.system_channel.send(embed=eMessage)

#If needed, will resend the welcome message
@client.hybrid_command(brief='Resend welcome message', description='Sends my welcome message again, in case a new member missed it')
async def resend(ctx):
    eMessage = discord.Embed(description="{0}".format(greetMessage))
    eMessage.set_author(name='Timey', icon_url=timeyIcon)
    await ctx.send(embed=eMessage)

# TODO #21 port this module to the db
# ---------------- Sending random messages ----------------
#Bob Ross quote
@client.hybrid_command(brief='Quote Bob Ross', description='Sends a Bob Ross quote')
async def bobross(ctx):
# Posts quotes of Bob Ross
    embedRossIcon = "http://i.imgur.com/OZLdaSn.png"
    await ctx.send(embed=await createEmbedFromRandomLine(name='Bob Ross',icon=embedRossIcon, tableName='bobQuotes', columnName='quote'))


# TODO #22 port this module to the db
#Just sends a damn Bovonto pitch
@client.hybrid_command(brief='Pitch Bovonto', description='Sends a Bovonto advertising pitch')
async def bovonto(ctx):
    embedBovontoIcon = 'https://imgur.com/8aCQlV5.png'
    await ctx.send(embed=await createEmbedFromRandomLine(name='Bovonto Bot',icon=embedBovontoIcon, tableName='bovontoPitches', columnName='pitch'))

#---------------- Role management functions ----------------
#Adds a pronoun specific role
@client.hybrid_command(brief='Add pronoun role', description='Add a pronoun role to yourself')
async def callme(ctx, pronoun: str):
    user = ctx.message.author
    genderId = get(ctx.guild.roles, name=pronoun)
    #This checks the list of roles on the server and the order they're in. Do not fuck with the order on the server or this will fuck up.
    upperDemarc = get(ctx.guild.roles, name='he/him'); lowerDemarc = get(ctx.guild.roles, name='Catillac Cat')
    if genderId > upperDemarc or genderId <= lowerDemarc:
        await ctx.send('<:rudy:441453959215972352> Oooooh, {0} isn\'t as sneaky as they think they are. '.format(user.mention))
    elif genderId <= upperDemarc and genderId > lowerDemarc:
        userRoles = ctx.author.roles
        if genderId in userRoles:
            await ctx.send('<:rudy:441453959215972352> You already have {0} pronouns.'.format(pronoun))
        if genderId not in userRoles:
            await user.add_roles(genderId)
            await ctx.send('<:heathsalute:482273509951799296> Comrade {0} wants to be called {1}.'.format(user.mention, pronoun))

#Removes a pronoun specific role          
@client.hybrid_command(brief='Remove pronoun role', description='Remove a pronoun role from yourself')
async def imnot(ctx, old_pronoun: str):
    user = ctx.message.author
    roleToRemove = get(ctx.guild.roles, name=old_pronoun)
    userRoles = ctx.author.roles
    await user.remove_roles(roleToRemove)
    await ctx.send('<:heathsalute:482273509951799296> Comrade {0} no longer wants to be called {1}.'.format(user.mention, old_pronoun))
    if roleToRemove not in userRoles:
        await ctx.send("<:rudy:441453959215972352> You never picked those pronouns.")

#Adds a non-pronoun specific role
@client.hybrid_command(brief='Add other opt-in role', description='Join one of the other role-based groups')
async def join(ctx, new_role: str):
    user = ctx.message.author
    roleToAdd = get(ctx.guild.roles, name=new_role.lower())
    lowerDemarc = get(ctx.guild.roles, name='Catillac Cat')
    if roleToAdd >= lowerDemarc:
        await ctx.send("<:rudy:441453959215972352> That's not what this is for.")
    else:
        await user.add_roles(roleToAdd)
        await ctx.send('<:heathsalute:482273509951799296> {0} has joined {1}!'.format(user.mention, new_role))

#Removes a non-pronoun specific role
@client.hybrid_command(brief='Remove other opt-in role', description='Leave one of the other role-based groups')
async def leave(ctx, old_role: str):
    user = ctx.message.author
    roleToRemove = get(ctx.guild.roles, name=old_role.lower())
    userRoles = ctx.author.roles
    await user.remove_roles(roleToRemove)
    await ctx.send('{0} is no longer a member of {1}.'.format(user.mention, old_role))
    if roleToRemove not in userRoles:
        await ctx.send("<:rudy:441453959215972352> You were never in that role.")

#Lists unformatted all roles.  
@client.hybrid_command(brief='List all roles', description='List all roles on the server, joinable or otherwise')
async def listroles(ctx):
    rolesStr = ', '.join(map(lambda r: str(r), ctx.guild.roles))
    await ctx.send(rolesStr)

#---------------- Tarot functions ----------------
# single card draw
@client.hybrid_command(brief='Single card tarot draw', help='Draws a random card from a 78 card Rider-Waite tarot deck, including reversed cards.')
async def tarot(ctx):
    if '__template' in tarotData:
        await ctx.send('Oops, someone needs to put a proper tarot deck into my brain first!')
    else:
        if 'deck' in tarotData:
            card_index = random.randint(0, len(tarotData['deck'])-1)
            card = tarotData['deck'][card_index]
            emb = discord.Embed(type='rich', title=card['title'], description=card['meaning'], url=card['url'])
            emb.add_field(name='Keywords', value=', '.join(card['keywords']) )
            emb.add_field(name='Yes/No?', value=card['yesno'])
            emb.set_image(url=card['image'])
            emb.set_footer(text='Images © Labyrinthos LLC')
            await ctx.send('{0.display_name}, you have drawn: '.format(ctx.message.author), embed=emb)
        else:
            await ctx.send('Oops, I do not seem to have a valid tarot deck loaded, sorry!')

#Actually running the damn thing
client.run(os.environ['TOKEN'])
