import pygame
import os
import subprocess

import conf

class button():
    def __init__(self, size, color, textCol=conf.fontCol, text='', textSize=conf.fontSize, autoScale=True, ot=True):
        self.size       = size
        self.scaledSize = pygame.Rect(size[0],size[1],size[2],size[3])
        self.color      = color
        self.col        = color
        self.textCol    = textCol
        self.text       = text
        self.textSize   = textSize
        self.active     = False
        self.autoScale  = autoScale
        self.ot         = ot


    def draw(self, surface):
        scalingX            = conf.winSize[0] / conf.startWinSize[0]
        scalingY            = conf.winSize[1] / conf.startWinSize[1]
        if conf.winSize[1]  < conf.startWinSize[1]: #wacky clamp
            scalingY        = conf.startWinSize[1] / conf.startWinSize[1]

        self.scaledSize     = pygame.Rect(self.size[0]*scalingX, self.size[1]*scalingY - conf.scroll, 
                                           self.size[2]*scalingX, self.size[3]*scalingY)

        if self.ot:
            pygame.draw.rect(surface, conf.secondCol, self.scaledSize.inflate(scalingX*10, scalingY*10))
        pygame.draw.rect(surface, self.col, self.scaledSize)


        if self.text != '':
            fontText    = conf.makeText(self.text, self.textCol, int(self.textSize * (scalingY * 2)) )
            surface.blit(fontText, (self.scaledSize[0] + (self.scaledSize[2]/2 - fontText.get_width()/2), 
                                self.scaledSize[1] + (self.scaledSize[3]/2 - fontText.get_height()/2)
                                ))


    def hover(self, pos):
        if not self.active:
            if pos[0] > self.scaledSize[0] and pos[0] < self.scaledSize[0] + self.scaledSize[2]:
                if pos[1] > self.scaledSize[1] and pos[1] < self.scaledSize[1] + self.scaledSize[3]:
                    self.col = self.color[0] / 1.5, self.color[1] / 1.5, self.color[2] / 1.5
                    return True
            self.col = self.color
        else:
            self.col = self.color[0] / 1.5, self.color[1] / 1.5, self.color[2] / 1.5

        return False


    def click(self, event, pos):
        if self.hover(pos):
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                return True
        else:
            return False



def createVpnButts():
    offset = 100
    serverName = ''


    try:
        result = subprocess.run(
                'ip link show | awk -F: \'/wg/ && /UP/ {gsub(/ /,"",$2); print $2}\'',
                shell=True,
                capture_output=True,
                text=True
                )
        if result.stdout:
            conf.currentVpn = result.stdout.strip()
        
    except Exception as e:
        pass


    vpnButts.append( button( (0,offset, conf.startWinSize[0],60), conf.primeCol, text='Turn VPN off' ) )
    offset += 80

    for file in os.listdir(conf.vpnDir):
        if file.endswith('.conf'):

            filepath = os.path.join(conf.vpnDir, file)
            with open(filepath, 'r') as f:
                lines = f.readlines()
                for i, line in enumerate(lines):
                    if line.strip() == '[Peer]':
                        serverName  = lines[i + 1].strip()
                        #endpoint    = lines[i + 3].strip().split('=')[1].strip()
                        
                        break
            

            fileName = os.path.splitext(file)[0]

            vpnButts.append( button( (0,offset, conf.startWinSize[0],60), 
                                    conf.primeCol, text=str(f'{fileName} | {serverName}') ) )

            vpnNames.append(fileName)

            offset += 80



def wgQuickCommand(vpn, upORdown):
    subprocess.run([
                    'sudo',
                    'wg-quick',
                    upORdown,
                    f'{vpn}'
                        
                    ])


def getCurrentVpn(event, pos):
    try:
        for butt in vpnButts:

            if butt.click(event, pos):

                selectedVpn = vpnNames[vpnButts.index(butt)]
                
                if conf.currentVpn != 'No VPN' and conf.currentVpn != selectedVpn:
                    wgQuickCommand(conf.currentVpn, 'down')
                    
                if selectedVpn != 'No VPN':
                    wgQuickCommand(selectedVpn, 'up')
                            
                if selectedVpn == 'No VPN':
                    wgQuickCommand(conf.currentVpn, 'down')
                    
                conf.currentVpn = vpnNames[vpnButts.index(butt)]
                

            if conf.currentVpn == vpnNames[vpnButts.index(butt)]:
                butt.active = True
                conf.activeButt = butt.text

            else:
                butt.active = False


        if conf.currentVpn == 'No VPN':
            currentConnection.text = 'No VPN Connected'
 
        else:
            currentConnection.text = f'Connected to: {conf.activeButt}'

        
    except Exception as e:
        print("ERROR:", e)
        raise



vpnNames            = ['No VPN']
vpnButts            = []

currentConnection = button( (0,0, conf.startWinSize[0],70), conf.primeCol, text='No VPN Connected' )

