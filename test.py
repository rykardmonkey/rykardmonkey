import classes.swgohhelp as swg
import json
import os
from datetime import datetime

swgohhelp_username = ''
swgohhelp_password = ''

with open('credentials.config') as configData:
    configJSON = json.load(configData)
    print()
