import discord
import json

client = None
async def do_ping(self, u, g, c, arg):
    response = 'Pong, `{0}ms`!'.format(round(client.latency * 1000))
    embed=discord.Embed(
        title="Command Result from {0}".format(u.name),
        description=response,
        color=discord.Color.blue()
    )
    await c.send(embed=embed)

async def list_commands(self, u, g, c, arg):
    embed=discord.Embed(
        title="Command List",
        description="`The valid list of commands are:`\n\n",
        color=discord.Color.green()
    )
    for cmd in commands.keys():
        embed.description = embed.description + ":crown: **" + cmd + "**" + "\n"
    await c.send(embed=embed)

def read_json(arg):
    try:
        with open("/home/pi/DiscordPyBot/Data/"+arg+'.json', 'r+') as json_file:
            return json.load(json_file)
    except:
        return False

def save_json(arg, json_string):
    try:
        with open("/home/pi/DiscordPyBot/Data/"+arg+'.json', 'w+') as json_file:
            return json.dump(json_string, json_file)
    except:
        return False

def create_json(arg):
    with open("/home/pi/DiscordPyBot/Data/"+arg+".json", 'w+') as json_file:
        json_file.write('{"data": [], "schedule": {"Sunday": "yes", "Monday": "yes", "Tuesday": "yes", "Wednesday": "yes", "Thursday": "yes", "Friday": "yes", "Saturday": "yes"}}')
        return json.load(json_file)

def check_data(u):
    Data = read_json(str(u.id))
    if Data == False:
        Data = create_json(str(u.id))
    return Data

async def get_info(self, u, g, c, arg):
    Data = check_data(u)
    weekEmbed = discord.Embed(
        title = "Schedule",
        description="This is `{0}'s` schedule availablity.\n".format(u.display_name),
        color=discord.Color.purple()
    )
    for day in Data["schedule"]:
        emoji = ":red_square:"
        dayInfo = str(Data["schedule"][day])
        if dayInfo == "yes":
            emoji = ":green_square:"
        elif dayInfo == "maybe":
            emoji = ":orange_square:"
        weekEmbed.description = weekEmbed.description + "**{0}:** {1} \n".format(day, emoji)
    #save_json(str(u.id), Data)
    await c.send(embed=weekEmbed)

async def set_avail(self, u, g, c, arg):
    Weekdays = {"sunday": False,"monday": False,"tuesday": False,"wednesday": False,"thursday": False,"friday": False,"saturday": False,}
    if len(arg) == 2 and str(arg[0]) in Weekdays.keys():
        Data = check_data(u)
        WeekdayStr = arg[0][0:1].upper() + arg[0][1:]
        if str(arg[1]) == "no" or str(arg[1]) == "yes" or str(arg[1]) == "maybe":
            Data["schedule"][WeekdayStr] = str(arg[1])

        save_json(str(u.id), Data)
        await c.send("You have successfully set `{0}` avaliability to `{1}`".format(WeekdayStr, arg[1].upper()))

commands = {
    'ping': do_ping,
    'cmds': list_commands,
    'info': get_info,
    'set': set_avail
    #'read_json': read_json
}

class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))

    async def on_message(self, message):
        prefix = "!"
        if message.author == self.user:
            return
        if not message.content.startswith(prefix):
            return
        content = message.content[1:].lower()
        author = message.author
        guild = message.guild
        channel = message.channel
        arguments = content.split(" ")
        command =  arguments[0]
        if len(message.mentions) != 0 and command == "info":
            author = message.mentions[0]
        del arguments[0]
        if command in commands.keys():
            try:
                await commands[command](self, author, guild, channel, arguments)
            except Exception as e:
                print(e)
                await channel.send(str(e))
                #await channel.send("The command you have used has experienced an error.\n")
        else:
            await channel.send("Invalid Command, try again. :tada:")
        #print('Message from {0.author}: {0.content}'.format(message))

client = MyClient()
client.run("--BASTARDED TOKEN")
