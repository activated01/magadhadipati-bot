########### IMPORTING-LIBRARIES ###########
import discord
import os
from discord.ext import commands

# from keep_alive import keep_alive

########### Instance of Intents and enabling the necessary ones ###########
intents = discord.Intents.default()
intents.guilds = True
intents.members = True
intents.message_content = True

########### SECRET-KEYS ###########
from dotenv import load_dotenv
load_dotenv()
token = os.getenv("SECRET_KEY")


# Initialize the bot with a command prefix and the specified intents
bot = commands.Bot(command_prefix="!", intents=intents)

################################
########### CHANNELS ###########
################################
server_channel_id = 1198343760724103178
rules_channel_id = 1200897973975007372
announcement_channel_id = 1198343661453328615
roles_channel_id = 1198343092143653036
updates_channel_id = 1198362311904198756
welcome_channel_id = 1196193311367647316
intro_channel_id = 1196200169071444018


####################### ROLES-ID #######################
roles = {
    "🔰": 1198340951291199579,    ## Magahiya
    "🔍": 1254798912749961277,    ## Bhashavid
    
    "🌟": 1254795480525832302,    ## Kritikaar
    "📝": 1254798543416459365,    ## Wikikaar
    "🔄": 1254798717752709172,    ## Anuvadak

    "🎉": 1254806196666503188,    ## Ayojak
}

######################################################
####################### EVENTS #######################
######################################################

########### ON-READY ###########
@bot.event
async def on_ready():
    print(f'Bot is ready. Logged in as {bot.user.name}')

    #############################################
    ################### ROLES ###################
    channel = bot.get_channel(roles_channel_id)

    # Check if the message ID file exists
    if os.path.exists("message_id.txt"):
        with open("message_id.txt", "r") as file:
            message_id = int(file.read().strip())

        # Try to fetch the message
        try:
            message = await channel.fetch_message(message_id)
            print("Role assignment message already exists.")
        except discord.NotFound:
            message = await send_role_message(channel)
            save_message_id(message.id)
    else:
        message = await send_role_message(channel)
        save_message_id(message.id)

async def send_role_message(channel, edit=False):
    embed = discord.Embed(
        title="अपन भूमिका चुनी",
        description="भाषा भूमिका :\n"
                    "🔰: मगहिया (यदि अपने मगही जानही - Magahiya)\n"
                    "🔍: भाषाविद् (भाषाज्ञाता - Linguist)\n\n"

                    "जोगदान भूमिका :\n"
                    "🌟: कृतिकार (मगहीके कृतिकार - Content Creator)\n"
                    "📝: विकिकार (विकिपीडिया आदि जोगदानकर्ता - Wikipedian)\n"
                    "🔄: अनुवादक (मगहीके अनुवादक - Translator)\n\n"

                    "सर्वर भूमिका :\n"
                    "🎉: आयोजक (कार्यक्रम आयोजक - event organiser)\n",
        color=0x00ff00
    )

    # Send a new message or edit the existing one based on 'edit' flag
    if edit:
        message = await channel.fetch_message(edit)
        await message.edit(embed=embed)
    else:
        message = await channel.send(embed=embed)
        for emoji in roles.keys():
            await message.add_reaction(emoji)

    return message

def save_message_id(message_id):
    with open("message_id.txt", "w") as file:
        file.write(str(message_id))

@bot.command(name='update_roles')
@commands.has_permissions(administrator=True)
async def update_roles(ctx):
    channel = ctx.channel

    # Check if the message ID file exists
    if os.path.exists("message_id.txt"):
        with open("message_id.txt", "r") as file:
            message_id = int(file.read().strip())

        # Edit the existing message with updated roles
        message = await send_role_message(channel, edit=message_id)
        save_message_id(message.id)
        await ctx.send("Role assignment message updated.")
    else:
        message = await send_role_message(channel)
        save_message_id(message.id)
        await ctx.send("Role assignment message created and saved.")

@bot.event
async def on_raw_reaction_add(payload):
    if payload.user_id == bot.user.id:
        return

    guild = bot.get_guild(payload.guild_id)
    role_id = roles.get(payload.emoji.name)
    if role_id is None:
        return

    role = guild.get_role(role_id)
    if role is None:
        return

    member = guild.get_member(payload.user_id)
    if member is None:
        return

    await member.add_roles(role)

@bot.event
async def on_raw_reaction_remove(payload):
    if payload.user_id == bot.user.id:
        return

    guild = bot.get_guild(payload.guild_id)
    role_id = roles.get(payload.emoji.name)
    if role_id is None:
        return

    role = guild.get_role(role_id)
    if role is None:
        return

    member = guild.get_member(payload.user_id)
    if member is None:
        return

    await member.remove_roles(role)
    ################ ROLES ENDS #################
    #############################################

    # Retrieve channels once the bot is ready
    bot.server_channel = bot.get_channel(server_channel_id)
    bot.rules_channel = bot.get_channel(rules_channel_id)
    bot.announcement_channel = bot.get_channel(announcement_channel_id)
    bot.roles_channel = bot.get_channel(roles_channel_id)
    bot.updates_channel = bot.get_channel(updates_channel_id)
    bot.welcome_channel = bot.get_channel(welcome_channel_id)
    bot.intro_channel = bot.get_channel(intro_channel_id)

############################################
################# COMMANDS #################
############################################
## !hello ##
@bot.command(name='नमस्कार',
             aliases=[
                 'नमस्ते', 'नमस्कारम्', 'प्रणाम', 'परनाम', 'namaskar',
                 'namaskara', 'namaste', 'namaskaram', 'pranam', 'pranaam',
                 'pranaama', 'pranama', 'parnam', 'padnam', 'parnama',
                 'paranam', 'hello', 'hi', 'hey', 'greetings'
             ])
async def hello(ctx):
    await ctx.send('नमस्कार, हम एगो बाॅट् हियो !')


########### WELCOME-MESSAGE ###########
@bot.event
async def on_member_join(member):

    if bot.welcome_channel and isinstance(bot.welcome_channel,
                                          discord.TextChannel):
        await bot.welcome_channel.send(
            f'नमस्कार {member.mention} जी ! मगधादिपति सर्वरमे अपनेके स्वागत हे । अपने <#{roles_channel_id}> मे अपना लागि भूमिका लेके <#{intro_channel_id}> मे अपन परिचय दे सकही । सर्वरके नियम पढ़ेला <#{rules_channel_id}> पर जायी ।'
        )


######################################################
######################################################
######################################################

########### KEEP-ALIVE ###########
# keep_alive()

########### RUN ########### 
bot.run(token)
