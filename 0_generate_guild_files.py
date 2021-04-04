import classes.swgohhelp as swg
import json
import os
from datetime import datetime

GUILD_FILE_PATH = './data pull/'
PLAYER_FILE_PATH = './data pull/members/'
BATTLE_FILE_PATH = './data pull/battles/'

# support functions
def connect_to_client():
    swgohhelp_username = ''
    swgohhelp_password = ''

    with open('credentials.config') as configData:
        configJSON = json.load(configData)
        startingAllyCode = configJSON['swgoh']['allycode']
        swgohhelp_username = configJSON['swgohhelp']['username']
        swgohhelp_password = configJSON['swgohhelp']['password']

    credentials = swg.settings(swgohhelp_username,swgohhelp_password,'123','abc')
    return startingAllyCode, swg.SWGOHhelp(credentials)

def generate_data_file(filePath, fileName, dataType, allycode, client, verbose):
    if os.path.isfile(filePath + fileName) == False:
        if verbose == True: print(dataType,' file: ',fileName,' does not exist, generating..')
        player = client.get_data('player',allycode)
        fileFullPath = filePath + fileName
        with open(fileFullPath,'w') as outfile:
            json.dump(player, outfile, indent=4)
    else:
        if verbose == True: print(dataType,' file: ',fileName,' exists, continue on..')

def verify_directory_exists(filePath):
    if not os.path.exists(filePath):
        os.makedirs(filePath)

def main():
    # intialize client
    startingAllyCode, client = connect_to_client()

    verify_directory_exists(GUILD_FILE_PATH)
    verify_directory_exists(PLAYER_FILE_PATH)
    verify_directory_exists(BATTLE_FILE_PATH)
    
    # generating guild file based on my allycode
    guildFileName = 'guild.json'
    generate_data_file(GUILD_FILE_PATH, guildFileName, 'guild', startingAllyCode, client, True)

    print('generate all guild member objects..')
    with open(GUILD_FILE_PATH + guildFileName,'r') as guildFileData:
        guildData = json.load(guildFileData)
        rosterJsonList = guildData[0]['roster']

        for i in rosterJsonList:
            guildAllyCode = int(i['allyCode'])

            # remove special characters from the name before using to generate filename
            guildAllyName = "".join(x for x in i['name'] if x.isalnum())
            
            guildAllyFileName = guildAllyName + '.player.' + str(guildAllyCode) + '.json'
            generate_data_file(PLAYER_FILE_PATH, guildAllyFileName, 'player', guildAllyCode, client, False)

            # no point doing battles it is identical to players
            # battleAllyFileName = guildAllyName + '.battles.' + str(guildAllyCode) + '.json'
            # generate_data_file(BATTLE_FILE_PATH, battleAllyFileName, 'battles', guildAllyCode, client, True)

if __name__ == "__main__":
    main()
