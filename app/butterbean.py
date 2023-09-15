#Butterbean DiscordBot for WATTBA Discord 
#author: Tupperward

#Importing dependencies
from importlib.metadata import MetadataPathFinder
import discord, os , random, asyncio
from discord.ext import commands, tasks
from discord.utils import get

from modules.tarot_data import tarotData

from sqlalchemy import create_engine, table, text
from sqlalchemy.orm import Session

from github import Github


#-----------Buttons!-----------#
bovontoSchedule = False

#-----------Get privileged intents so we can be in compliance with the API  -----------#
intents = discord.Intents.default()
intents.messages = True
intents.members = True
intents.message_content = True  

#-----------Intializing functions-----------#
client = commands.Bot(command_prefix=('/','!'), description='Butterborg is online.', add=True, intents=intents)

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

access_token = os.environ.get('GITHUB_ACCESS_TOKEN')
repo_name = os.environ.get('GITHUB_REPO_NAME')
mod_name = os.environ.get('MOD_NAME')
bot_mod_name = os.environ.get('BOT_MOD_NAME')
restricted_roles = ['sheriff','admin','Da Hosts','Dr. Wily','technomancer','PatreonBot','bird-expert','time-out-corner','Butterborg']
welcome_channel_id = 465991895693393929
emojis = ['😎', '😇', '😊', '🧐', '🤩', '😏', '😩', '😤', '👐', '🤟', '👏', '🖖', '🙌', '🤙', '🦾']
role_emojis = {
    f"{emojis[0]}": "any/all",
    f"{emojis[1]}": "he/",
    f"{emojis[2]}": "she/",
    f"{emojis[3]}": "they/",
    f"{emojis[4]}": "xe/",
    f"{emojis[5]}": "ze/",
    f"{emojis[6]}": "fae/",
    f"{emojis[7]}": "it/",
    f"{emojis[8]}": "/him",
    f"{emojis[9]}": "/her",
    f"{emojis[10]}": "/them",
    f"{emojis[11]}": "/xer",
    f"{emojis[12]}": "/zir",
    f"{emojis[13]}": "/faer",
    f"{emojis[14]}": "/its",
}
greetMessage = "Welcome to the WATTBA-sistance! Please take your time to read #rules-and-info and then, if you're comfortable, use the **/pickpronoun** command to privately tag yourself with your pronouns." + "\n\nYou can also react to this message with your pronouns. This server allows you to set a primary and secondary pronoun role, with your name changing color to reflect your primary pronouns." + "\n\n**Primary Pronouns:** (pick just one)\n😎: `any/all`  😇: `he/` 😊: `she/` 🧐: `they/` 🤩: `xe/` 😏: `ze/` 😩: `fae/` 😤: `it/`" +  "\n\n**Secondary Pronouns:** (pick as many as you'd like!)\n 👐: `/him` 🤟: `/her` 👏: `/them` 🖖: `/xer` 🙌: `/zir` 🤙: `/faer` 🦾: `/its`" + "\n\nFeel free to reach out to any of our mods for any reason, they're always happy to talk: criss (@.crissxcore), mx. president (@kbuechner) or AR (@armoredrobot)." + "\n\nThis server also uses this bot for meme purposes. Be on the lookout for memes you can send using by sending **/bb** and the name of the meme. You can find a list of those memes with **/beanfo**. __I'll be honest, most of these are currently broken because of imgur deleting basically everything__."
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
async def has_role(member, role_name) -> bool:
    # Check if the member object has the role with the specified name
    role = discord.utils.get(member.roles, name=role_name)
    return role is not None

async def getRowCount(tableName: str) -> int:
    statement = "SELECT COUNT(*) FROM {}".format(tableName)
    with Session(engine) as session:
        result = session.execute(statement).fetchone()
    return result[0]

async def pickRandomRow(tableName: str, columnName: str) -> str:
    totalRows = await getRowCount(tableName)
    randomLine = random.randint(1,totalRows)
    statement = "SELECT {} FROM {} WHERE id={};".format(columnName, tableName, randomLine)
    with Session(engine) as session:
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
    if await has_role(member=ctx.message.author, role_name=mod_name) or await has_role(member=ctx.message.author, role_name=bot_mod_name):
        with Session(engine) as session:
            session.begin()
            lookupString = "INSERT INTO posts (post_name, link) VALUES ('{0}','{1}');".format(name, url)
            session.execute(text(lookupString))
            session.commit()
            await ctx.send("{} has been added to my necroborgic memories".format(name))
    else:
        await ctx.send(unapprovedDeny.format(ctx.message.author))

#Mods can remove items from the list
@client.hybrid_command(brief='Remove a meme', description='Removes a meme from my necroborgic memories, if you have permission')
async def remove (ctx, meme: str): 
    if await has_role(member=ctx.message.author, role_name=mod_name) or await has_role(member=ctx.message.author, role_name=bot_mod_name):
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
@client.event 
async def on_raw_reaction_add(payload):
    if payload.channel_id == welcome_channel_id:
        guild = client.get_channel(payload.channel_id).guild
        member = guild.get_member(payload.user_id)

        emoji = payload.emoji.name 
        if emoji in role_emojis:
            role_name = role_emojis[emoji]
            role = discord.utils.get(guild.roles, name=role_name)

            if role: 
                await member.add_roles(role)
                print(f"{member.name} has been assigned the {role_name} role.")

@client.event 
async def on_raw_reaction_remove(payload):
    if payload.channel_id == welcome_channel_id:
        guild = client.get_channel(payload.channel_id).guild
        member = guild.get_member(payload.user_id)

        emoji = payload.emoji.name 
        if emoji in role_emojis:
            role_name = role_emojis[emoji]
            role = discord.utils.get(guild.roles, name=role_name)

            if role and role in member.roles: 
                await member.remove_roles(role)
                print(f"{member.name} has removed the {role_name} role.")               

#Welcomes a new member
@client.event
async def on_member_join(member):
    guild = member.guild
    if guild.system_channel is not None:
        embed = discord.Embed(description=f"{on_member_join.mention}! {greetMessage}")
        embed.set_author(name='Timey', icon_url=timeyIcon)
        message = await guild.system_channel.send(embed=embed)
        for emoji in emojis:
            await message.add_reaction(emoji)

#If needed, will resend the welcome message
@client.hybrid_command(brief='Resend welcome message', description='Sends my welcome message again, in case a new member missed it')
async def welcome(ctx):
    embed = discord.Embed(description=f"{greetMessage}")
    embed.set_author(name='Timey', icon_url=timeyIcon)
    message = await ctx.send(embed=embed)
    for emoji in emojis:
        await message.add_reaction(emoji)

# ---------------- Sending random messages ----------------
#Bob Ross quote
@client.hybrid_command(brief='Quote Bob Ross', description='Sends a Bob Ross quote')
async def bobross(ctx):
# Posts quotes of Bob Ross
    embedRossIcon = "http://i.imgur.com/OZLdaSn.png"
    await ctx.send(embed=await createEmbedFromRandomLine(name='Bob Ross',icon=embedRossIcon, tableName='bobQuotes', columnName='quote'))

#Just sends a damn Bovonto pitch
@client.hybrid_command(brief='Pitch Bovonto', description='Sends a Bovonto advertising pitch')
async def bovonto(ctx):
    embedBovontoIcon = 'https://imgur.com/8aCQlV5.png'
    await ctx.send(embed=await createEmbedFromRandomLine(name='Bovonto Bot',icon=embedBovontoIcon, tableName='bovontoPitches', columnName='pitch'))

#Adds a non-pronoun specific role
@client.hybrid_command(brief='Add other opt-in role', description='Join one of the other role-based groups')
async def join(ctx, new_role: str):
    user = ctx.message.author
    roleToAdd = get(ctx.guild.roles, name=new_role.lower())
    if roleToAdd in restricted_roles:
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

#---------------- Create Github Issue ----------------

@client.hybrid_command(brief='Create a ticket in Github', description='Creates a ticket for project tracking in Butterbeans Github repository')
async def create_ticket(ctx, title: str, body: str):
    g = Github(access_token)
    repo = g.get_repo(repo_name)
    repo.create_issue(title=title, body=body)
    await ctx.send(f'Created ticket named: `{title}`')

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

#----- Pronoun Picker -----

# our pronoun picker feature needs a "view" to be able to display some UI components; this one just inherits straight from
#  discord.ui.View, but adds an extra constructor, since we need to pass the interaction along when creating the dropdown -
#  otherwise, it won't have any way to find out what server the request came from
class PronounPickerView(discord.ui.View):
    def __init__(self, interaction: discord.Interaction):
        super().__init__()

        # add the dropdown to our view
        self.add_item(PronounPicker(interaction))

# this is the dropdown used to select your roles and placed in the view
class PronounPicker(discord.ui.Select):
    def __init__(self, interaction: discord.Interaction):

        # get all the settable roles that look like pronouns
        valid_pronouns = list(filter(lambda r: r.is_assignable() and (r.name.find('/') > -1) and (not r.name in restricted_roles), reversed(interaction.guild.roles)))

        # Set the options that will be presented inside the dropdown
        options = []

        # TODO: if there's no emoji set for the role, perhaps we can try to map role colour to a coloured shape emoji?
        for p in valid_pronouns:
            l = p.name            # role name
            e = p.unicode_emoji   # associated emoji, if any
            checked = (p in interaction.user.roles) # if the user currently has this role, present a checked box
            options.append(discord.SelectOption(label=l, emoji=e, description=f'Tag me as {l}, please', default=checked))

        # construct a Select object for the UI to use which the user can select any number of options from, including zero
        #   to remove all tags
        super().__init__(placeholder='Choose which pronoun sets you\'d like to have', min_values=0, max_values=len(options), options=options)
   
    # when the user finishes making their selection, this callback fires
    async def callback(self, interaction: discord.Interaction):

        # get all the settable roles that look like pronouns
        valid_pronouns = list(filter(lambda r: r.is_assignable() and (r.name.find('/') > -1) and (not r.name in restricted_roles), reversed(interaction.guild.roles)))

        # check whether we need to set and/or unset each pronoun
        for p in valid_pronouns:
            if p.name in self.values:
                # this pronoun is in the list of wanted pronouns, add it if necessary
                if not (p in interaction.user.roles):
                    await interaction.user.add_roles(p, reason=f'Added by {interaction.user.name} via pronoun picker')
            else:
                # this pronoun is not wanted, remove it if necessary
                if (p in interaction.user.roles):
                    await interaction.user.remove_roles(p, reason=f'Removed by {interaction.user.name} via pronoun picker')

        # show confirmation to the user (that only the user can see)
        await interaction.response.send_message(f'Your pronouns are now {", ".join(self.values) if len(self.values) > 0 else "(none)"}', ephemeral=True)


# add the slash command to the bot's command tree
@client.tree.command(description='Get a menu to pick your pronouns from')
async def pickpronoun(interaction: discord.Interaction):
    # create the UI and show it to the user (and only the user, via the ephemeral flag)
    view = PronounPickerView(interaction)
    await interaction.response.send_message('Please choose any number of pronouns:', view=view, ephemeral=True)


#Actually running the damn thing
client.run(os.environ['TOKEN'])
