import pygame

from pathlib import Path
import configparser
import shutil
import sys
import ast

configPath  = Path.home() / '.config' / 'gooeyplate'
configFile  = configPath / 'gooeyplate.conf'
vpnDirPath  = configPath / 'vpns'
fontFile    = next(configPath.glob('*.ttf'), None) #font is jack input 



def getSelfPath(relativePath):
    if hasattr(sys, '_MEIPASS'):
        return Path(sys._MEIPASS) / relativePath
    return Path(__file__).parent / relativePath



def isConfigThere(fontFile):
    configPath.mkdir(parents=True, exist_ok=True)

    vpnDirPath.mkdir(parents=True, exist_ok=True)

    if not configFile.exists():
        defaultConfig   = getSelfPath('gooeyplate.conf')
        shutil.copy(defaultConfig, configFile)
    
    config      = configparser.ConfigParser()
    config.read(configFile)
    
    if ast.literal_eval(config['FONT']['font']) == 'system-font':
        fontFile        = 'system-font'
    elif fontFile == None:
        defaultFont     = getSelfPath('defaultFont.ttf')
        if defaultFont.exists():
            shutil.copy(defaultFont, configPath / 'defaultFont.ttf')
            fontFile    = next(configPath.glob('*.ttf'), None)
            #if you are building this yourself or just running the python file you can
            #remove the defaultFont.ttf from the directory if you want to use system font
            #for a more lightweight option
    return config, fontFile



config, fontFile = isConfigThere(fontFile)
config.read(configFile)


startWinSize    = ast.literal_eval(config['MAIN']['starting-window-size'])
winSize         = startWinSize

if fontFile == 'system-font':
    font        = None

elif fontFile.exists() and fontFile != 'system-font':
    font        = configPath / ast.literal_eval(config['FONT']['font'])
    if font != fontFile:
        font    = None

else:
    font        = None


fontSize        = ast.literal_eval(config['FONT']['font-size'])

primeCol        = ast.literal_eval(config['COLOR']['button-color'])
secondCol       = ast.literal_eval(config['COLOR']['accent-color'])
backCol         = ast.literal_eval(config['COLOR']['background-color'])
fontCol         = ast.literal_eval(config['COLOR']['font-color'])

scroll          = 0 
scrollMod       = ast.literal_eval(config['MAIN']['scroll-modifier'])

vpnDir          = vpnDirPath
currentVpn  = 'No VPN'
activeButt  = 'None'


def makeText(text, color, size):
    fonty   = pygame.font.Font(font, size)
    return fonty.render(text, True, color)
