import classes.swgohhelp as swg
import json
import os
from datetime import datetime

GUILD_FILE_PATH = './data pull/'
PLAYER_FILE_PATH = './data pull/members/'

# get my own data first
allycode = 877541847

# support functions
def connect_to_client():
    swgohhelp_username = ''
    swgohhelp_password = ''

    with open('credentials.config') as configData:
        configJSON = json.load(configData)
        swgohhelp_username = configJSON['swgohhelp']['username']
        swgohhelp_password = configJSON['swgohhelp']['password']

    credentials = swg.settings(swgohhelp_username,swgohhelp_password,'123','abc')
    return swg.SWGOHhelp(credentials)

def generate_data_file(filePath, fileName, dataType, allycode, client):
    if os.path.isfile(filePath + fileName) == False:
        print(dataType,' file: ',fileName,' does not exist, generating..')
        player = client.get_data('player',allycode)
        fileFullPath = filePath + fileName
        with open(fileFullPath,'w') as outfile:
            json.dump(player, outfile, indent=4)
    else:
        print(dataType,' file: ',fileName,' exists, continue on..')

def main():
    # intialize client
    client = connect_to_client()

    # generating guild file based on my allycode
    guildFileName = 'guild.json'
    generate_data_file(GUILD_FILE_PATH, guildFileName, 'guild', allycode, client)

    print('retrieve just the ally codes of all members..')
    with open(GUILD_FILE_PATH + guildFileName,'r') as guildFileData:
        guildData = json.load(guildFileData)
        rosterJsonList = guildData[0]['roster']

        for i in rosterJsonList:
            guildAllyCode = int(i['allyCode'])
            # if it is not me, go create a file for them
            if (guildAllyCode != allycode):
                # remove special characters from the name before using to generate filename
                guildAllyName = "".join(x for x in i['name'] if x.isalnum())
                
                guildAllyFileName = guildAllyName + '.player.' + str(guildAllyCode) + '.json'
                generate_data_file(PLAYER_FILE_PATH, guildAllyFileName, 'player', guildAllyCode, client)

if __name__ == "__main__":
    main()
