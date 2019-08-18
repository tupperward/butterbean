#Butterbean DiscordBot for WATTBA Discord 
#author: Tupperward
#content contributor: Smoltz, Jackapedia

#Thank you to Agnes(Smyrna) for providing guidance throughout the whole process

#Importing dependencies
import discord; import os; import pickle; from bobross import rossQuotes; from bobross import embedRossIcon; import random
from discord.ext import commands
from discord.utils import get

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

#Message Send with !bb arg
@client.command()
async def bb(ctx, arg):
    dictIn = open('dict.pickle', 'rb')
    butterBeanDict = pickle.load(dictIn)
    await ctx.send(butterBeanDict.get(arg))
    dictIn.close()

#Mods can add items to the list
@client.command()
async def add(ctx, key, val):
    namesIn = open('names.pickle','rb')
    approvedUsers = pickle.load(namesIn)
    if str(ctx.message.author) in approvedUsers:
        dictIn = open('dict.pickle', 'rb')
        butterBeanDict = pickle.load(dictIn)
        update = {key : val}
        butterBeanDict.update(update)
        dictOut = open('dict.pickle','wb')
        pickle.dump(butterBeanDict, dictOut)
        dictOut.close()
        await ctx.send("%s has been added to my necroborgic memories" % (key))
    else:
        await ctx.send("Uh uh uh! " + ctx.message.author.mention + " didn't say the magic word!")
        await ctx.send("https://imgur.com/IiaYjzH")
    namesIn.close()

@client.command()
async def remove (ctx, key):
    namesIn = open('names.pickle','rb')
    approvedUsers = pickle.load(namesIn)
    if str(ctx.message.author) in approvedUsers:
        dictIn = open('dict.pickle','rb')
        butterBeanDict = pickle.load(dictIn)
        del butterBeanDict[key]
        dictOut = open('dict.pickle','wb')
        pickle.dump(butterBeanDict, dictOut)
        dictOut.close()
        await ctx.send("%s has been purged from my necroborgic memories" % (key))
    else:
        await ctx.send("Uh uh uh! " + ctx.message.author.mention + " didn't say the magic word!")
        await ctx.send("https://imgur.com/IiaYjzH")
    namesIn.close()

@client.command()
async def beanfo(ctx):
    #embed = discord.Embed(title='List of commands', color=0xeee657)
    dictIn = open('dict.pickle','rb')
    butterBeanDict = pickle.load(dictIn)
    count = 0
    necroborgicMemory = ""
    for memory in butterBeanDict.keys():
        count += 1
        if not count % 4 == 0:
            necroborgicMemory += memory + " "*(20-len(memory)) + ", "
        else:
            necroborgicMemory += memory + " "*(20-len(memory)) + "\n"
    await ctx.send(necroborgicMemory)
    dictOut = open('dict.pickle','wb')
    pickle.dump(butterBeanDict, dictOut)
    dictOut.close()

@client.event
async def on_member_join( member):
    guild = member.guild
    if guild.system_channel is not None:
        eMessage = discord.Embed(description="{0.mention}! Welcome to the WATTBA-sistance! Please take your time to observe our rules and, if you're comfortable, use the **!callme** command to tag yourself with your pronouns. Available pronouns are **he/him**, **she/her**, **they/them**, **xe/xem** and **ze/zir** If you get tired of your pronouns you can remove them with **!imnot** \n\n There are several other roles you can **!join** too, like **Streampiggies** to be notified of Eli's streams. Check them out by using **!listroles**. \n\n Oh, and feel free to get an inspirational Bob Ross quote any time with **!bobross**.".format(member))
        await guild.system_channel.send(embed=eMessage)

@client.command()
async def resend(ctx):
    eMessage = discord.Embed(description="Welcome to the WATTBA-sistance! Please take your time to observe our rules and, if you're comfortable, use the **!callme** command to tag yourself with your pronouns. Available pronouns are **he/him**, **she/her**, **they/them**, **xe/xem** and **ze/zir** If you get tired of your pronouns you can remove them with **!imnot** \n\n There are several other roles you can **!join** too, like **Streampiggies** to be notified of Eli's streams. Check them out by using **!listroles**. \n\n Oh, and feel free to get an inspirational Bob Ross quote any time with **!bobross**.")
    await ctx.send(embed=eMessage)

@client.command()
async def bobross (ctx):
# Posts quotes of Bob Ross
    rand_c = random.randint(0, len(rossQuotes) - 1)
    quote = rossQuotes[rand_c]
    e = discord.Embed(description=quote)
    e.set_author(name="Bob Ross", icon_url=embedRossIcon)
    await ctx.send(embed=e)

#Role management functions
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
          
@client.command()
async def imnot(ctx, oldRole):
    user = ctx.message.author
    roleToRemove = discord.utils.get(ctx.guild.roles, name=oldRole)
    userRoles = ctx.author.roles
    await user.remove_roles(roleToRemove)
    await ctx.send('<:heathsalute:482273509951799296> Comrade {0} no longer wants to be called {1}.'.format(user.mention, oldRole))
    if roleToRemove not in userRoles:
        await ctx.send("<:rudy:441453959215972352> You never picked those pronouns.")

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

@client.command()
async def leave(ctx, oldRole):
    user = ctx.message.author
    roleToRemove = discord.utils.get(ctx.guild.roles, name=oldRole.lower())
    userRoles = ctx.author.roles
    await user.remove_roles(roleToRemove)
    await ctx.send('{0} is no longer a member of {1}.'.format(user.mention, oldRole))
    if roleToRemove not in userRoles:
        await ctx.send("<:rudy:441453959215972352> You were never in that role.")
  
@client.command()
async def listroles(ctx):
    roleList = ''
    roles = ctx.guild.roles
    for i in roles:
        roleList += " " + str(i) +","
    await ctx.send(roleList)

#Actually running the damn thing

client.run(os.environ['BOT_TOKEN'])
