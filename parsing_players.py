import json
import os
import glob
from datetime import datetime

PLAYER_FILE_PATH = './data pull/members/'

# support functions
def get_filename_list(filePath):
    fileList = []
    for f in os.listdir(filePath):
        if (os.path.isfile(filePath + f)):
            fileList.append(f)

    return fileList

# main process
def main():
    playerFileList = get_filename_list(PLAYER_FILE_PATH)
    print(playerFileList)

    for i in playerFileList:
        

if __name__ == "__main__":
    main()




