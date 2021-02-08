import discord
import json
import requests
client = discord.Client()

#instantiate the bot
@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

#respond to stuff here
@client.event
async def on_message(message):

    #dont talk to yourself
    if message.author == client.user:
        return

    #This isn't important functionality but useful to quickly check bot health
    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

    #Get the little lore blurb in the champ file
    #only workable format is $loreme name name2
    #but it wont crash if thats not what you get


    if message.content.startswith('$loreme'):
        name = message.content
        splitname = namecheck(name)
        champURL = "http://ddragon.leagueoflegends.com/cdn/{}/data/en_US/champion/{}.json"
        champName = splitname[1]
        getVersion = requests.get("https://ddragon.leagueoflegends.com/realms/na.json")
        ddVersion = getVersion.json()['dd']
        response = requests.get(champURL.format(ddVersion,champName))
        print(champName)
        try:
            
            data = response.json()
            await message.channel.send(data['data'][champName]['lore'])
        except:
            await message.channel.send("Didn't find that.")

    #get the ability info
    #format is $skills name(if its sol xin or j4 concatenates the names) abilitykey
    if message.content.startswith('$skills'):
        name = message.content
        splitname = namecheck(name)
        direction = 'C:/Users/jense/Documents/DataDragon/11.1.1/data/en_US/champion/{}.json'
        ability = {
            'q': 0,
            'w': 1,
            'e': 2,
            'r': 3
        }
        whichspell = ability[splitname[2]]
        #couple test prints for relevant variables
        # print(whichspell)
        # print(direction.format(splitname[1]))
        # print(splitname[1])
        try:
            with open(direction.format(splitname[1])) as f:
                data = json.load(f)
                await message.channel.send(data['data'][splitname[1]]['spells'][whichspell]['cooldown'])
        except:
            await message.channel.send("Didn't find that.")

def namecheck(name):
    splitname = name.lower().split(" ")
    splitname[1] = splitname[1].capitalize()
    if(splitname[1] == 'Aurelion' or splitname[1] == 'Jarvan' or splitname[1] == 'Xin'):
        splitname[1] = splitname[1] + splitname.pop(2).capitalize()
    #why is it like this?
    if(splitname[1] == 'Wukong'):
        splitname[1] = 'MonkeyKing'
    return splitname

client.run('ODA3MDI2Njc3MjAwNzE1Nzg3.YByAKQ.S_dNhcCdFgYFEQAwMNJ8HDLWydU')