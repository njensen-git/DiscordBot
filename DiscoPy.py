import discord
import json
import requests
import youtube.dl
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

    if message.content.startswith('$commands'):
        await message.channel.send('$skills Name Ability for skill cds and such\n$loreme Name for lore blurb')

    #Get the little lore blurb in the champ file
    if message.content.startswith('$loreme'):
        info = message.content
        infoList = namecheck(info)
        champName = infoList[0]
        champInfo = getChampInfo(champName)
        print(champName)
        print(champInfo.json()['data'])
        try:
            data = champInfo.json()
            await message.channel.send(data['data'][champName]['lore'])
        except:
            await message.channel.send("Didn't find that.")

    #get the ability info
    #format is $skills name(if its sol xin or j4 concatenates the names) abilitykey
    if message.content.startswith('$skills'):
        info = message.content
        #list of gained info in form of [name,ability]
        infoList = namecheck(info)
        champName = infoList[0]
        champInfo = getChampInfo(champName)
        abilityName = infoList[1]

        ability = {
            'q': 0,
            'w': 1,
            'e': 2,
            'r': 3
        }
        try:
            whichspell = ability[abilityName]
        except:
            await message.channel.send("Not an ability?")
        try:
            data = champInfo.json()
            skillNameData = str(data['data'][champName]['spells'][whichspell]['name'])
            cdData = str(data['data'][champName]['spells'][whichspell]['cooldown'])
            costData =  str(data['data'][champName]['spells'][whichspell]['cost'])
            rangeData =  str(data['data'][champName]['spells'][whichspell]['range'])
            await message.channel.send(skillNameData + "\nCD: " + cdData + "\nCost: " + costData + "\nRange: " + rangeData)
        except:
            await message.channel.send("Didn't find that.")

def namecheck(name):
    splitname = name.lower().split(" ")
    splitname.pop(0)
    splitname[0] = splitname[0].capitalize()
    if(splitname[0] == 'Aurelion' or splitname[0] == 'Jarvan'):
        splitname[0] = splitname[0] + splitname.pop(1).capitalize()
    if(splitname[0] == 'Twisted' or splitname[0] == 'Xin'):
        splitname[0] = splitname[0] + splitname.pop(1).capitalize()  
    if(splitname[0] == 'Tahm' or splitname[0] == 'Miss'):
        splitname[0] = splitname[0] + splitname.pop(1).capitalize()  
    if(splitname[0] == 'Master' or splitname[0] == 'Lee'):
        splitname[0] = splitname[0] + splitname.pop(1).capitalize()  
    if(splitname[0] == 'Dr'):
        splitname[0] = splitname[0] + splitname.pop(1).capitalize()  
    #why is it like this?
    if(splitname[0] == 'Wukong'):
        splitname[0] = 'MonkeyKing'
    #nobody uses their real names
    if(splitname[0] == 'Tf'):
        splitname[0] = 'TwistedFate'
    if(splitname[0] == 'Yi'):
        splitname[0] = 'MasterYi'
    if(splitname[0] == 'Kog'):
        splitname[0] = 'KogMaw'
    if(splitname[0] == 'Kogmaw'):
        splitname[0] = 'KogMaw'
    if(splitname[0] == 'Mundo'):
        splitname[0] = 'DrMundo'
    if(splitname[0] == 'Cass'):
        splitname[0] = 'Cassiopeia'
    if(splitname[0] == 'Cho'):
        splitname[0] = 'Chogath'
    return splitname

def getChampInfo(name):
    champURL = "http://ddragon.leagueoflegends.com/cdn/{}/data/en_US/champion/{}.json"
    getVersion = requests.get("https://ddragon.leagueoflegends.com/realms/na.json")
    ddVersion = getVersion.json()['dd']
    response = requests.get(champURL.format(ddVersion,name))
    return response

client.run('ODA3MDI2Njc3MjAwNzE1Nzg3.YByAKQ.S_dNhcCdFgYFEQAwMNJ8HDLWydU')